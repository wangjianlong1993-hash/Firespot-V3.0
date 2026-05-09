"use client";

import { useCallback, useMemo, useState, useEffect } from "react";
import type { Message } from "@langchain/langgraph-sdk";
import {
  CheckCircle2Icon,
  XCircleIcon,
  RefreshCwIcon,
  Loader2Icon,
  FileTextIcon,
} from "lucide-react";

import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { useThread } from "./context";
import { extractTextFromMessage } from "@/core/messages/utils";
import { cn } from "@/lib/utils";

interface FireSpotReviewDialogProps {
  message: Message;
  threadId: string;
}

type ApprovalAction = "approve" | "revise" | "cancel";

interface ParsedApprovalRequest {
  stage: string;
  description: string;
  reviewPath?: string;
  wechatPath?: string;
}

/**
 * Parse FireSpot approval request message content.
 * Expected format:
 * 📝 Stage 6: Review & Approval
 *
 * Article review is ready for your approval.
 *
 * Review: /mnt/user-data/outputs/stage6_review.html
 * WeChat: /mnt/user-data/outputs/stage6_wechat_draft.html
 *
 * Please choose:
 * ✅ Approve - Proceed to Stage 7 (AI image generation)
 * ✏️ Revise - Request revisions with specific feedback
 * ❌ Cancel - Terminate the workflow
 */
function parseApprovalMessage(
  content: string,
): ParsedApprovalRequest | null {
  const lines = content.split("\n").map((line) => line.trim());

  // Check if this is a FireSpot approval request (v7.1: Stage 6 or Stage 8)
  if (!content.includes("Stage") && !content.includes("Review & Approval") && !content.includes("Merge & Preview")) {
    return null;
  }

  let stage = "Stage 6";
  let description = "";
  let reviewPath: string | undefined;
  let wechatPath: string | undefined;

  // Detect stage (v7.1: Stage 6 for text review, Stage 8 for merge preview)
  if (content.includes("Stage 8") || content.includes("Merge & Preview")) {
    stage = "Stage 8";
  } else if (content.includes("Stage 6")) {
    stage = "Stage 6";
  }

  // Extract description and file paths
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    // Extract review path
    if (line.toLowerCase().includes("review:") && line.includes("/")) {
      const match = line.match(/\/[^\s]+/);
      if (match) {
        reviewPath = match[0];
      }
    }

    // Extract WeChat path
    if (line.toLowerCase().includes("wechat:") && line.includes("/")) {
      const match = line.match(/\/[^\s]+/);
      if (match) {
        wechatPath = match[0];
      }
    }

    // Build description (skip the header line and file path lines)
    if (
      line &&
      !line.includes("Stage 6") &&
      !line.includes("Stage 8") &&
      !line.toLowerCase().startsWith("review:") &&
      !line.toLowerCase().startsWith("wechat:") &&
      !line.match(/^\d+\./) &&
      !line.includes("━") &&
      !line.includes("═") &&
      !line.startsWith("✅") &&
      !line.startsWith("✏️") &&
      !line.startsWith("❌")
    ) {
      if (description) {
        description += " " + line;
      } else {
        description = line;
      }
    }
  }

  return {
    stage,
    description: description.trim() || "Article review is ready for your approval.",
    reviewPath,
    wechatPath,
  };
}

/**
 * Get button styling for action type.
 */
function getButtonVariant(action: ApprovalAction): "default" | "outline" | "destructive" {
  switch (action) {
    case "approve":
      return "default";
    case "revise":
      return "outline";
    case "cancel":
      return "destructive";
  }
}

/**
 * Get icon for action type.
 */
function getActionIcon(action: ApprovalAction) {
  switch (action) {
    case "approve":
      return CheckCircle2Icon;
    case "revise":
      return RefreshCwIcon;
    case "cancel":
      return XCircleIcon;
  }
}

/**
 * FireSpotReviewDialog component displays a modal dialog for Stage 6/8 approval
 * with three clickable options: approve, revise, cancel.
 *
 * v7.1 Updates:
 * - High-quality writing style: Real cases, specific data, vivid details
 * - Strictly avoids low-level AI expressions
 * - Stage 6: Text review approval → triggers Stage 7 (AI image generation)
 * - Stage 8: Merge preview approval → triggers Stage 9 (WeChat publishing)
 * - Button labels and descriptions updated for new workflow
 */
export function FireSpotReviewDialog({
  message,
  threadId,
}: FireSpotReviewDialogProps) {
  const { thread } = useThread();
  const [isOpen, setIsOpen] = useState(true);
  const [isResponding, setIsResponding] = useState(false);

  const content = extractTextFromMessage(message);
  const parsed = useMemo(() => {
    if (!content) return null;
    return parseApprovalMessage(content);
  }, [content]);

  // Check if thread is currently streaming
  const isStreaming = thread.isLoading;

  // Auto-open dialog when approval request appears
  useEffect(() => {
    if (parsed && !isStreaming) {
      setIsOpen(true);
    }
  }, [parsed, isStreaming]);

  const handleActionClick = useCallback(
    async (action: ApprovalAction) => {
      if (isResponding || isStreaming) return;

      setIsResponding(true);

      try {
        // Dispatch custom event for parent component to handle
        const event = new CustomEvent("firespot-approval-response", {
          detail: { action, threadId, message },
        });
        window.dispatchEvent(event);

        // Close dialog after a short delay to show feedback
        setTimeout(() => {
          setIsOpen(false);
        }, 300);
      } catch (error) {
        console.error("Failed to send approval response:", error);
        setIsResponding(false);
      }
    },
    [isResponding, isStreaming, threadId, message],
  );

  if (!parsed) {
    return null;
  }

  const actions: { key: ApprovalAction; label: string; description: string }[] = [
    {
      key: "approve",
      label: parsed.stage === "Stage 6" ? "✅ 批准 (Approve)" : "✅ 批准发布 (Approve)",
      description: parsed.stage === "Stage 6" ? "文字稿符合要求，自动进入Stage 7生成图片" : "图文合并预览符合要求，继续发布流程",
    },
    {
      key: "revise",
      label: "✏️ 修改 (Revise)",
      description: parsed.stage === "Stage 6" ? "需要修改内容，返回Stage 4重新创作" : "需要修改，重新生图或修改内容",
    },
    {
      key: "cancel",
      label: "❌ 取消 (Cancel)",
      description: "终止当前工作流程",
    },
  ];

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DialogContent
        className="sm:max-w-[600px] bg-black border-gray-800"
        onPointerDownOutside={(e) => e.preventDefault()}
        onEscapeKeyDown={(e) => e.preventDefault()}
      >
        <DialogHeader>
          <div className="flex items-center gap-3">
            <FileTextIcon className="size-6 text-white" />
            <div>
              <DialogTitle className="text-white text-xl">
                {parsed.stage} - {parsed.stage === "Stage 6" ? "文字稿审核" : "图文合并审核"}
              </DialogTitle>
              <DialogDescription className="text-gray-400 text-sm">
                FireSpot v7.1 内容创作工作流
              </DialogDescription>
            </div>
          </div>
        </DialogHeader>

        <div className="py-6 space-y-4">
          {/* Description */}
          <p className="text-gray-200 text-sm leading-relaxed">
            {parsed.description}
          </p>

          {/* File paths (if available) */}
          {(parsed.reviewPath || parsed.wechatPath) && (
            <div className="space-y-2 bg-gray-900/50 p-3 rounded border border-gray-800">
              {parsed.reviewPath && (
                <div className="flex items-center gap-2 text-xs">
                  <span className="text-gray-400">📄 审核版本:</span>
                  <span className="text-gray-300 font-mono">
                    {parsed.reviewPath.split("/").pop()}
                  </span>
                </div>
              )}
              {parsed.wechatPath && (
                <div className="flex items-center gap-2 text-xs">
                  <span className="text-gray-400">💬 微信版本:</span>
                  <span className="text-gray-300 font-mono">
                    {parsed.wechatPath.split("/").pop()}
                  </span>
                </div>
              )}
            </div>
          )}

          {/* Action prompt */}
          <p className="text-gray-400 text-sm">请选择下一步操作:</p>
        </div>

        <DialogFooter className="flex-col gap-3 sm:gap-2">
          {actions.map((action) => {
            const ActionIcon = getActionIcon(action.key);
            return (
              <Button
                key={action.key}
                variant={getButtonVariant(action.key)}
                onClick={() => handleActionClick(action.key)}
                disabled={isResponding || isStreaming}
                className={cn(
                  "w-full h-auto py-4 px-6 justify-start",
                  action.key === "approve" && "bg-green-600 hover:bg-green-700 text-white border-0",
                  action.key === "revise" && "bg-gray-800 hover:bg-gray-700 text-white border-gray-700",
                  action.key === "cancel" && "bg-red-900/50 hover:bg-red-900/70 text-white border-red-800",
                )}
              >
                <div className="flex items-start gap-3 w-full">
                  {isResponding ? (
                    <Loader2Icon className="size-5 animate-spin mt-0.5" />
                  ) : (
                    <ActionIcon className="size-5 mt-0.5 flex-shrink-0" />
                  )}
                  <div className="flex-1 text-left">
                    <div className="font-medium text-base">{action.label}</div>
                    <div className="text-xs opacity-80 mt-0.5">
                      {action.description}
                    </div>
                  </div>
                </div>
              </Button>
            );
          })}
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

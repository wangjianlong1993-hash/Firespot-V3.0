# Changelog

All notable changes to FireSpot Agent Skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [7.2.0] - 2026-05-09

### 🎉 Major Release - 工作流优化

### ✨ Added
- **ZhipuArts MCP专业生图** - 集成智谱AI GLM-Image，专业科技风格图片生成
- **自动发布功能** - 支持一键发布到微信公众号草稿箱
- **模块化设计** - 清晰的工作流阶段分离，易于维护和扩展
- **README.md** - 完整的项目说明文档
- **package.json** - 标准化的包配置文件
- **CHANGELOG.md** - 版本变更记录文档

### 🔄 Changed
- **工作流从10阶段调整为9阶段**
  - 移除原阶段6：排版预览
  - 重新编号：阶段7-10 → 阶段6-9
- **SKILL.md更新**
  - 更新核心工作流程图
  - 移除排版预览章节
  - 更新参数清单（排版要求：不包含排版设计）
  - 更新输出文件数量（4个 → 3个）
  - 移除排版相关的脚本和模板引用
- **workflow_v7.2.md更新**
  - 删除阶段6排版预览完整章节
  - 更新阶段依赖关系图
  - 更新关键流程节点描述
  - 移除排版模板扩展机制章节
  - 清理退出条件中的"跳过排版"选项
- **INDEX.md更新**
  - 删除layout_guide.md的文档条目
  - 更新工作流阶段列表（10阶段 → 9阶段）
  - 移除排版规范相关的文档分类
- **mcp_tools_guide.md更新**
  - 更新代码示例（从读取排版预览改为读取文章内容）

### 🗑️ Removed
- **阶段6：排版预览** - 完全移除排版设计工作流
- **references/layout_guide.md** - 排版规范指南文档
- **assets/config/layout_config.json** - 排版配置文件
- **assets/scripts/generate_layout.py** - 排版生成脚本
- **assets/prompts/stage6_layout.txt** - 阶段6排版提示词模板
- **assets/templates/layout_template.html** - 排版HTML模板
- **.DS_Store文件** - 清理macOS系统文件

### 📝 Technical Details
- **工作流优化原则**：专注内容创作和AI生图，排版设计由用户自行处理
- **向后兼容性**：保留v7.1版本的9阶段工作流文档作为参考
- **MCP工具依赖**：ZhipuArts MCP作为推荐图片生成方案
- **文档完整性**：所有文档已更新以反映9阶段工作流

### 📊 Statistics
- **文件变更**：删除5个排版相关文件，新增3个文档文件
- **代码行数**：SKILL.md从~500行优化到~450行
- **工作流阶段**：10阶段 → 9阶段
- **输出文件**：4个 → 3个
- **文档数量**：保持9份参考文档

---

## [7.1.0] - Earlier Release

### ✨ Added
- **初始版本** - 7阶段标准化工作流
- **基础内容创作功能** - 研究到校验的完整流程
- **AI生图功能** - 支持多种AI图片生成方案
- **排版预览功能** - 自动应用品牌排版规范
- **微信公众号发布** - 支持自动发布草稿

### 📋 Features
- 阶段0：参数收集
- 阶段1：多平台热点研究
- 阶段2：内容分析
- 阶段3：内容规划
- 阶段4：内容创作
- 阶段5：合规校验
- 阶段6：排版预览
- 阶段7：人工审核
- 阶段8：AI生图
- 阶段9：图文合并
- 阶段10：自动发布

---

## 📅 Release Timeline

| Version | Release Date | Status | Description |
|---------|--------------|--------|-------------|
| 7.2.0 | 2026-05-09 | ✅ Current | 工作流优化，移除排版，专注内容和AI生图 |
| 7.1.0 | Earlier | 📜 Legacy | 初始版本，完整10阶段工作流 |

---

## 🔮 Future Plans

### v7.3.0 (Planned)
- [ ] 支持更多AI图片生成模型
- [ ] 增强内容质量评估机制
- [ ] 优化工作流执行效率
- [ ] 增加更多发布平台支持

### v8.0.0 (Long-term)
- [ ] 多语言内容创作支持
- [ ] 自定义工作流编排
- [ ] 协作编辑功能
- [ ] 内容效果分析

---

## 📞 Feedback & Support

- **问题反馈**: [GitHub Issues](https://github.com/your-org/firespot/issues)
- **功能建议**: [GitHub Discussions](https://github.com/your-org/firespot/discussions)
- **邮件联系**: your-email@example.com

---

**Note**: 版本号遵循语义化版本规范 (Semantic Versioning)：
- **MAJOR**: 不兼容的API更改
- **MINOR**: 向后兼容的功能新增
- **PATCH**: 向后兼容的问题修复

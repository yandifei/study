const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, HeadingLevel, PageNumber, PageBreak,
  TableOfContents, BorderStyle, WidthType, ShadingType, LevelFormat
} = require('docx');

// ========================
// FONT HELPERS
// ========================
// Default: 宋体 (eastAsia) + Times New Roman (ascii), 12pt = 24 half-pts
const DEF_FONT = { ascii: "Times New Roman", eastAsia: "宋体", hAnsi: "Times New Roman", cs: "Times New Roman" };
const HEI_FONT = { ascii: "Times New Roman", eastAsia: "黑体", hAnsi: "Times New Roman", cs: "Times New Roman" };
const KAI_FONT = { ascii: "Times New Roman", eastAsia: "楷体", hAnsi: "Times New Roman", cs: "Times New Roman" };
const FANG_FONT = { ascii: "Times New Roman", eastAsia: "仿宋_GB2312", hAnsi: "Times New Roman", cs: "Times New Roman" };

function txt(text, opts = {}) {
  return new TextRun({
    text,
    font: opts.font || DEF_FONT,
    size: opts.size || 24,        // 12pt
    bold: opts.bold || false,
    italics: opts.italics || false,
    ...opts.extra || {}
  });
}

function boldTxt(text, opts = {}) {
  return txt(text, { ...opts, bold: true });
}

function para(text, opts = {}) {
  const runs = Array.isArray(text) ? text : [txt(text, opts)];
  return new Paragraph({
    children: runs,
    alignment: opts.align || AlignmentType.JUSTIFIED,
    spacing: opts.spacing || { line: 360, lineRule: "auto" },
    indent: opts.indent || (opts.firstLine !== false ? { firstLine: 480 } : undefined),
    ...opts.extra || {}
  });
}

function heading1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    children: [txt(text, { font: HEI_FONT, size: 30, bold: true })],
    alignment: AlignmentType.LEFT,
    spacing: { before: 240, after: 120, line: 360, lineRule: "auto" }
  });
}

function heading2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    children: [txt(text, { font: HEI_FONT, size: 28, bold: true })],
    alignment: AlignmentType.LEFT,
    spacing: { before: 200, after: 100, line: 360, lineRule: "auto" }
  });
}

function heading3(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_3,
    children: [txt(text, { font: HEI_FONT, size: 24, bold: true })],
    alignment: AlignmentType.LEFT,
    spacing: { before: 160, after: 80, line: 360, lineRule: "auto" }
  });
}

function emptyPara() {
  return new Paragraph({ children: [], spacing: { line: 360, lineRule: "auto" } });
}

// ========================
// CONTENT SECTIONS
// ========================
const KEYWORDS_CN = "微信小程序；ACG智能图廊；FastAPI；MongoDB；Dify大模型；多模态AI对话；SSE流式输出";
const KEYWORDS_EN = "WeChat Mini Program; ACG Smart Gallery; FastAPI; MongoDB; Dify LLM Platform; Multimodal AI Dialogue; SSE Streaming";

function buildCoverPage() {
  return [
    emptyPara(), emptyPara(),
    new Paragraph({
      children: [txt("期末大作业", { font: DEF_FONT, size: 52, bold: true })],
      alignment: AlignmentType.CENTER,
      spacing: { line: 440, lineRule: "exact" }
    }),
    emptyPara(), emptyPara(),
    new Paragraph({
      children: [txt("题    目          基于微信小程序的ACG智能图廊系统的设计与实现", { font: DEF_FONT, size: 28 })],
      spacing: { line: 440, lineRule: "exact" }
    }),
    emptyPara(),
    new Paragraph({
      children: [txt("二级学院        数据科学与计算机学院", { font: DEF_FONT, size: 28 })],
      spacing: { line: 440, lineRule: "exact" }
    }),
    emptyPara(),
    new Paragraph({
      children: [txt("专    业             软件工程", { font: DEF_FONT, size: 28 })],
      spacing: { line: 440, lineRule: "exact" }
    }),
    emptyPara(),
    new Paragraph({
      children: [txt("学    号             20235120801082", { font: DEF_FONT, size: 28 })],
      spacing: { line: 440, lineRule: "exact" }
    }),
    emptyPara(),
    new Paragraph({
      children: [txt("姓    名             潘炜德", { font: DEF_FONT, size: 28 })],
      spacing: { line: 440, lineRule: "exact" }
    }),
    emptyPara(),
    new Paragraph({
      children: [txt("指导教师              王亚萍  硕士", { font: DEF_FONT, size: 28 })],
      spacing: { line: 440, lineRule: "exact" }
    }),
    emptyPara(), emptyPara(), emptyPara(), emptyPara(),
    new Paragraph({
      children: [txt("2026 年 6 月  18 日", { font: DEF_FONT, size: 24 })],
      alignment: AlignmentType.CENTER,
      spacing: { line: 360, lineRule: "auto" }
    }),
    emptyPara(),
    new Paragraph({
      children: [txt("广东培正学院教务处", { font: DEF_FONT, size: 24 })],
      alignment: AlignmentType.CENTER,
      spacing: { line: 360, lineRule: "auto" }
    }),
  ];
}

function buildChineseTitle() {
  return [
    new Paragraph({ children: [new PageBreak()] }),
    emptyPara(), emptyPara(),
    new Paragraph({
      children: [txt("基于微信小程序的ACG智能图廊系统的设计与实现", { font: KAI_FONT, size: 44 })],
      alignment: AlignmentType.CENTER,
      spacing: { before: 240, after: 240 }
    }),
    emptyPara(),
    new Paragraph({
      children: [txt("潘炜德", { font: KAI_FONT, size: 24 })],
      alignment: AlignmentType.CENTER
    }),
    emptyPara(),
  ];
}

function buildAbstractCN() {
  return [
    new Paragraph({
      children: [boldTxt("摘要：", { font: DEF_FONT, size: 24 })],
      spacing: { line: 360, lineRule: "auto" },
      indent: { firstLine: 480 }
    }),
    new Paragraph({
      children: [txt(`随着人工智能技术的快速发展与移动互联网的深度融合，传统图片浏览类应用已难以满足用户对智能化、个性化交互体验的需求。本文设计并实现了一款基于微信小程序的"ACG智能图廊"系统，将ACG（动画、漫画、游戏）图片鉴赏与多模态AI对话能力有机融合，打造一个"可看、可聊、可思考"的智能图廊应用。系统采用微信小程序作为前端载体，后端基于FastAPI框架构建微服务架构，通过Nginx反向代理实现请求路由分发，使用MongoDB存储用户与图片数据、Redis管理会话与验证码缓存，并集成Dify大模型平台提供多模态AI对话服务。系统实现了邮箱验证码登录、JWT双Token无感刷新认证、主题分类图片浏览、收藏与浏览记录管理、基于SSE流式协议的AI图片鉴赏对话、多轮会话历史管理、AI思考过程折叠展示、消息反馈评价等核心功能。在部署层面，系统采用Docker容器化Nginx并结合Ngrok内网穿透技术，实现了从本地开发到公网HTTPS服务的完整链路。本文从需求分析、系统架构设计、数据库设计、关键功能实现到测试部署进行了全面阐述，为类似微信小程序结合大模型AI服务的应用开发提供了完整的技术参考。`, { font: DEF_FONT, size: 24 })],
      spacing: { line: 360, lineRule: "auto" },
      indent: { firstLine: 480 }
    }),
    emptyPara(),
    new Paragraph({
      children: [
        boldTxt("关键词：", { font: DEF_FONT, size: 24 }),
        txt(KEYWORDS_CN, { font: DEF_FONT, size: 24 })
      ],
      spacing: { line: 360, lineRule: "auto" },
      indent: { firstLine: 480 }
    }),
  ];
}

function buildAbstractEN() {
  return [
    emptyPara(), emptyPara(),
    new Paragraph({
      children: [txt("Design and Implementation of ACG Smart Gallery System Based on WeChat Mini Program", { font: DEF_FONT, size: 30, bold: true })],
      alignment: AlignmentType.CENTER,
      spacing: { before: 240, after: 240 }
    }),
    new Paragraph({
      children: [txt("By", { font: DEF_FONT, size: 24, bold: true, italics: true })],
      alignment: AlignmentType.CENTER
    }),
    new Paragraph({
      children: [txt("Pan Weide", { font: DEF_FONT, size: 24, bold: true })],
      alignment: AlignmentType.CENTER
    }),
    new Paragraph({
      children: [txt("June, 2026", { font: DEF_FONT, size: 24, bold: true })],
      alignment: AlignmentType.CENTER
    }),
    emptyPara(),
    new Paragraph({
      children: [boldTxt("Abstract: ", { font: DEF_FONT, size: 24 })],
      spacing: { line: 360, lineRule: "auto" },
      indent: { firstLine: 480 }
    }),
    new Paragraph({
      children: [txt(`With the rapid development of artificial intelligence technology and the deep integration of mobile internet, traditional image browsing applications can no longer meet users' demands for intelligent and personalized interactive experiences. This paper designs and implements an "ACG Smart Gallery" system based on WeChat Mini Program, which organically integrates ACG (Animation, Comic, Game) image appreciation with multimodal AI dialogue capabilities, creating an intelligent gallery application that is "viewable, conversational, and thoughtful". The system adopts WeChat Mini Program as the front-end carrier, with the back-end built on the FastAPI framework in a microservice architecture. Nginx reverse proxy handles request routing and distribution, MongoDB stores user and image data, Redis manages sessions and verification code caching, and the Dify LLM platform is integrated to provide multimodal AI dialogue services. The system implements core features including email verification code login, JWT dual-token seamless refresh authentication, theme-categorized image browsing, favorites and browsing history management, AI-powered image appreciation dialogue based on SSE streaming protocol, multi-turn conversation history management, AI thought process collapsible display, and message feedback rating. At the deployment level, the system employs Docker containerized Nginx combined with Ngrok intranet penetration technology, achieving a complete chain from local development to public HTTPS service. This paper provides a comprehensive exposition from requirements analysis, system architecture design, database design, key feature implementation to testing and deployment, offering a complete technical reference for similar WeChat Mini Program applications integrated with LLM AI services.`, { font: DEF_FONT, size: 24 })],
      spacing: { line: 360, lineRule: "auto" },
      indent: { firstLine: 480 }
    }),
    emptyPara(),
    new Paragraph({
      children: [
        boldTxt("Keywords: ", { font: DEF_FONT, size: 24 }),
        txt(KEYWORDS_EN, { font: DEF_FONT, size: 24 })
      ],
      spacing: { line: 360, lineRule: "auto" },
      indent: { firstLine: 480 }
    }),
  ];
}

// ========================
// CHAPTER 1: 概述
// ========================
function buildChapter1() {
  return [
    heading1("1 概述"),
    heading2("1.1 研究背景"),
    para(`随着移动互联网技术的迅猛发展和智能终端设备的全面普及，微信作为国内领先的社交平台，其月活跃用户于2023年已突破13亿。2017年微信小程序的正式推出，以其"即用即走、无需安装"的轻量化特性，迅速成为连接线上服务与线下场景的重要桥梁。在图像消费领域，ACG（动画、漫画、游戏）文化在年轻群体中影响力日益扩大，用户对图片浏览类应用的需求已从简单的"看图"升级为"懂图""聊图"——即希望获得对图片风格、技法、创作背景的深度解读，以及与AI进行个性化对话的能力。`),
    para(`与此同时，大语言模型（LLM）技术的突破性进展使得多模态AI对话成为可能。以Dify等开源平台为代表的大模型应用开发框架，大幅降低了AI应用的开发门槛，使个人开发者也能快速构建具备图像理解、自然语言对话等智能能力的应用。然而，目前市面上的图片浏览类小程序普遍存在功能单一、缺乏智能交互、前后端耦合度高、认证机制薄弱等问题，难以满足用户对智能化、个性化体验的期待。`),
    para(`基于上述背景，本文提出并实现了一款面向ACG爱好者的"ACG智能图廊"微信小程序，以ACG图片为核心内容载体，以多模态AI对话为核心交互方式，深度融合图片浏览与AI智能服务，旨在为用户提供一种全新的"可看、可聊、可思考"的图片鉴赏体验。同时，本文在系统架构设计、前后端解耦、JWT双Token认证、SSE流式对话、容器化部署等方面进行了较为全面的技术探索与实践，以期为同类应用的开发提供参考。`),

    heading2("1.2 研究意义"),
    para(`本课题的研究意义主要体现在以下三个层面。`),
    para(`在应用价值层面，ACG智能图廊系统精准定位于ACG爱好者、画师、图片收藏者及AI技术兴趣用户群体，通过将静态图片浏览与动态AI对话深度融合，创造了一种全新的交互模式。用户不仅能够按主题分类浏览高质量ACG图片资源，更能通过上传图片或输入文字与AI进行多模态对话，获取风格分析、构图解读、创作建议等智能服务。这种"图片为媒介、AI为能力"的设计理念，赋予了传统图片浏览应用以"智商"，提升了用户的使用体验与情感共鸣。`),
    para(`在技术实践层面，本系统采用当前业界主流的"微信小程序+FastAPI微服务+MongoDB+Redis+Dify大模型平台"技术栈，实现了一套完整的端到端服务架构。在认证机制上采用邮箱验证码登录与JWT双Token体系，兼顾了安全性与易用性；在AI对话实现上基于SSE流式协议，实现了类似ChatGPT的打字机效果与随时停止生成的能力；在部署方案上通过Nginx反向代理+Ngrok内网穿透，解决了开发阶段微信小程序要求HTTPS合法域名的痛点。这些技术方案均具有较强的通用性和参考价值。`),
    para(`在教育意义层面，本课题的完成过程涵盖需求分析、系统架构设计、数据库设计、前后端开发、测试部署、上线审核等软件工程的完整生命周期，是对本科阶段所学知识的综合运用与实践检验。从最初的"功能堆砌"思路到最终的"以图片为媒介、AI为能力"的融合设计，体现了软件工程中"想清楚再动手"的重要性。`),

    heading2("1.3 研究现状"),
    para(`在微信小程序生态领域，目前已有大量图片浏览类应用，涵盖了壁纸展示、相册管理、图片社区等多种形态。这些应用大多采用传统的客户端-服务器架构，前端以图片网格或瀑布流展示为主，后端通过RESTful API提供图片数据。在认证方面，多数小程序依赖于微信授权登录（wx.login），通过获取用户OpenID完成身份识别，开发调试较为便捷但扩展性受限。在数据存储方面，部分应用采用微信云开发（CloudBase）提供的数据库与存储服务，降低了后端运维成本。`),
    para(`然而，现有图片类小程序普遍存在以下不足：其一，功能同质化严重，大多数应用仅提供简单的图片浏览与收藏功能，缺乏智能化的内容理解与交互能力；其二，前后端耦合度高，业务逻辑与数据访问混杂，不利于系统的扩展与维护；其三，用户认证机制单一，过度依赖微信平台授权，限制了跨平台数据互通的可能性；其四，极少有应用尝试将大模型AI对话能力与图片浏览场景进行深度融合。`),
    para(`在大模型应用领域，以OpenAI的GPT系列、Anthropic的Claude系列为代表的大语言模型展现了强大的文本生成与多模态理解能力。Dify等开源LLM应用开发平台进一步降低了AI应用的门槛，提供了可视化的应用编排、对话管理、知识库检索等功能，并通过标准化的Service API支持第三方集成。然而，将此类平台与微信小程序深度结合、实现完整的用户认证、流式对话、会话管理等功能的实践案例仍然较少。本课题正是针对这一技术空白，进行了较为全面的探索与实践。`),
  ];
}

// ========================
// CHAPTER 2: 相关技术介绍
// ========================
function buildChapter2() {
  return [
    new Paragraph({ children: [new PageBreak()] }),
    heading1("2 相关技术介绍"),
    heading2("2.1 微信小程序"),
    para(`微信小程序是腾讯公司于2017年推出的一种不需要下载安装即可使用的轻量级应用，依托于微信生态系统运行。小程序采用原生框架开发，由WXML（视图层标记语言）、WXSS（样式语言）和JavaScript（逻辑层）三部分组成，通过双线程模型实现视图层与逻辑层的分离。本系统选择微信小程序作为前端载体，主要基于以下考量：其一，微信的庞大用户基础为应用提供了天然的流量入口；其二，小程序"即用即走"的特性契合图片浏览场景中碎片化、轻量化的使用需求；其三，微信小程序提供的开放能力（如震动反馈、剪切板操作、相册权限管理等）能够有效支撑本系统的交互设计。本系统要求微信客户端基础库版本不低于2.10.0，兼容iOS 12及以上和Android 8.0及以上操作系统。`),

    heading2("2.2 FastAPI 框架"),
    para(`FastAPI是一个基于Python 3.7+的现代化高性能Web框架，基于Starlette（异步Web框架）和Pydantic（数据校验库）构建。其核心优势包括：原生支持异步编程（async/await），能够高效处理并发I/O密集型任务；自动生成交互式OpenAPI文档（Swagger UI），便于开发阶段的接口调试；内置依赖注入机制（Depends），可实现优雅的认证中间件与路由解耦；类型提示（Type Hints）驱动的数据校验，减少了运行时错误。本系统选择FastAPI作为后端框架，充分利用其异步特性处理MongoDB数据操作与Redis缓存访问，利用依赖注入机制实现JWT认证中间件，并通过自动生成的API文档加速前后端联调。后端运行于Uvicorn ASGI服务器之上，Python版本要求3.14及以上。`),

    heading2("2.3 MongoDB 数据库"),
    para(`MongoDB是一个开源的NoSQL文档数据库，以灵活的JSON-like BSON文档格式存储数据，天然支持嵌入式文档和数组结构。本系统选择MongoDB而非传统关系型数据库，主要基于以下设计考量：其一，浏览记录和收藏记录是用户实体的强关联数据，采用嵌入式文档模式将二者嵌入User文档中，可以避免关系型数据库中频繁的JOIN操作，显著提升读取性能；其二，图片元数据具有半结构化特征，不同来源的图片可能包含差异化的属性字段，MongoDB的灵活Schema能够很好地适应这种数据异构性；其三，MongoDB提供的$push、$pull、$slice等原子操作符，能够高效地在服务端维护嵌入式数组的增删与分页，无需将全量数据拉回应用层处理。在驱动选择上，本系统使用pymongo 4.x自带的AsyncMongoClient原生异步驱动，替代已官方弃用的motor库，数据校验由Pydantic BaseModel负责而非使用ODM。`),

    heading2("2.4 Redis 缓存"),
    para(`Redis是一个开源的高性能键值对内存数据库，支持多种数据结构和丰富的原子操作。在本系统中，Redis承担以下关键职责：其一，Refresh Token会话存储，以Key格式"refresh:{user_id}:{jti}"存储有效的刷新令牌，支持精确撤销和全设备撤销（使用SCAN增量迭代而非阻塞式的KEYS命令）；其二，邮箱验证码临时存储，以Key格式"email_code:{email}"存储6位验证码，设置5分钟TTL自动过期，验证通过后立即删除实现一次性消费；其三，验证码发送冷却期控制，以Key格式"email_cooldown:{email}"设置60秒TTL，防止恶意频繁发送。在客户端选择上，本系统使用redis-py 8.x异步客户端，并显式设置protocol=2强制使用RESP2协议，规避RESP3协议在认证时序上的兼容性问题。`),

    heading2("2.5 Dify 大模型应用平台"),
    para(`Dify是一个开源的LLM应用开发平台，提供了可视化的应用编排界面和标准化的Service API。本系统选用Dify的对话型应用（Chat App）类型，其主要能力包括：支持多模态输入（文本+图片），能够调用具备Vision能力的大模型进行图文综合理解；内建会话持久化机制，自动管理多轮对话的上下文；支持SSE（Server-Sent Events）流式输出，实现逐Token推送的实时打字机效果；提供完整的会话管理API（历史消息查询、会话列表、会话删除、重命名）；支持消息反馈（点赞/点踩），便于优化模型输出质量；在Agent模式下还支持思考过程展示与工具调用。Dify通过Bearer API Key进行鉴权，本系统将API Key安全存储在后端环境变量中，前端不直接调用Dify API，而是经由自建的AI服务中转，增加了鉴权与用户映射层。`),

    heading2("2.6 Nginx 反向代理与 Ngrok 内网穿透"),
    para(`Nginx是一款高性能的HTTP和反向代理服务器，在本系统中作为统一入口网关，对外仅暴露单一端口（61000），通过URL路径前缀匹配将请求分发给不同的后端服务："/db/*"路径转发至数据库服务（端口21325），"/ai/*"路径转发至AI服务（端口21326），路径前缀在转发时自动剥离。Nginx通过Docker Compose进行容器化部署，使用nginx:stable-alpine镜像，通过host.docker.internal访问宿主机上的后端服务进程。Ngrok是一款内网穿透工具，能够在本地服务与公网之间建立安全的HTTPS隧道。在开发与演示阶段，Ngrok将本地Nginx的61000端口映射至公网HTTPS地址，解决了微信小程序后台要求配置HTTPS合法域名的约束，使开发调试无需部署到云服务器即可完成前后端联调。`),

    heading2("2.7 其他关键技术"),
    para(`本系统还涉及以下关键技术与工具库。python-jose库用于JWT的编码、解码和签名验证，支持HS256对称加密算法，较PyJWT具有更完善的Claims校验机制和异常体系，被FastAPI官方文档推荐。pydantic库作为FastAPI的底层数据校验引擎，其BaseModel类用于定义请求/响应模型、数据库文档映射模型，通过类型注解实现编译时与运行时的双重数据安全保障。python-dotenv库用于加载.env环境变量文件，将敏感凭证（邮箱SMTP密码、JWT签名密钥、Dify API Key、数据库连接字符串等）与代码分离。colorlog库提供彩色日志输出，便于开发阶段快速定位问题。QQ邮箱SMTP服务（smtp.qq.com:465，SSL加密）用于发送邮箱验证码，邮件内容基于HTML模板渲染。`),
  ];
}

// Chapter 3: 功能需求分析
function buildChapter3() {
  return [
    new Paragraph({ children: [new PageBreak()] }),
    heading1("3 功能需求分析"),
    heading2("3.1 需求概述"),
    para(`ACG智能图廊微信小程序的用户群体主要定位于ACG爱好者、画师创作人员、图片收藏爱好者以及对AI技术感兴趣的技术艺术交叉人群。系统需要满足的核心需求包括：为用户提供按主题分类的高质量ACG图片浏览体验；支持对图片进行收藏管理与浏览历史记录；提供基于大模型的多模态AI对话能力，使用户能够与AI深度交流图片的风格、技法、创作背景；支持流式输出以提升对话的实时感和交互体验；提供可靠的用户身份认证机制；确保游客用户的受限浏览权限与注册用户的完整体验。`),

    heading2("3.2 功能性需求"),
    heading3("3.2.1 用户认证模块"),
    para(`系统采用邮箱验证码登录机制替代传统的微信授权登录，用户输入邮箱地址后获取6位数字验证码，验证通过即完成登录，新用户自动注册。系统实现了严格的防刷机制：验证码发送设有60秒冷却期，验证码有效期为5分钟，验证通过后立即从Redis中删除（一次性消费），防止重放攻击。登录成功后签发JWT双Token：Access Token（有效期15分钟）用于API请求认证，Refresh Token（有效期30天，存储于Redis）用于无感刷新。Access Token过期后，前端请求拦截器自动调用刷新接口，用户无需手动重新登录。系统还支持单设备登出（撤销单个Refresh Token）和全设备登出（使用Redis SCAN命令增量撤销所有活跃会话）。`),

    heading3("3.2.2 首页主题导航模块"),
    para(`用户进入小程序首页后，系统展示图片分类主题入口列表，每个主题包含图标和名称。当前支持的主题类别包括：PC壁纸、AI生成图、AI竖屏图、白底极简、风景、风景竖屏、软萌表情、萌图、萌图竖屏、横屏壁纸、头像、原神横屏、原神竖屏等十余个分类维度，涵盖ACG二次元图片、自然风光、AI绘图等多种视觉艺术风格。用户点击任一主题卡片后跳转至图片鉴赏页并携带主题参数。在无网络连接时，系统使用本地缓存的主题列表作为兜底展示。`),

    heading3("3.2.3 图片鉴赏模块"),
    para(`图片鉴赏页接收主题参数（或搜索关键词），以两列网格布局分页展示图片缩略图。每屏默认加载约10张缩略图，滚动到底部自动触发下一页加载。点击任意缩略图弹出模态详情窗口，展示原图大图、AI预生成的描述文本、分类标签以及当前收藏状态。在详情弹窗中，用户可以点击收藏/取消收藏按钮进行操作，系统通过微信小程序震动API提供轻量级触觉反馈。收藏操作的API设计采用先$pull（按image_id去重）再$push+$sort的幂等模式，确保同一用户不会重复收藏同一图片。`),

    heading3("3.2.4 AI智能对话模块"),
    para(`AI智能对话模块是本系统的核心亮点。用户在搜索/探索页面可以输入文本或上传图片（最多3张），与Dify大模型进行多模态对话。系统采用SSE流式协议实现AI回复的逐字实时输出，产生类似打字机的视觉效果，并在回复末尾显示闪烁光标。用户可以随时点击停止按钮中断生成。对话支持多轮上下文记忆：首次对话自动创建新会话并返回conversation_id，后续消息携带该ID继续同一会话。系统还实现了侧边栏会话历史管理，支持会话列表展示（按更新时间倒序）、点击加载历史消息、左滑删除会话、新建空白会话等功能。AI回复中的思考过程（<think>标签包裹内容或Dify Agent模式的agent_thought事件）默认折叠展示为灰色胶囊按钮，用户点击可展开/收起，展开后内容可选中复制。此外，系统还支持对AI回复点赞/点踩的反馈评价（数据回传Dify后台）、一键复制回复内容、以相同参数重新生成回复等辅助功能。`),
  ];
}

// Chapter 3: 非功能性需求
function buildChapter3Continued() {
  return [
    heading2("3.3 非功能性需求"),
    heading3("3.3.1 性能需求"),
    para(`系统在性能方面设定了以下量化指标：图片网格首屏加载时间不超过2秒（4G网络，10张缩略图）；搜索/对话响应时间不超过3秒；图片详情弹窗打开时间不超过500毫秒（允许渐进显示原图）；页面切换动画帧率不低于30fps；验证码邮件发送时间不超过3秒；登录完成时间不超过2秒。系统设计支持不少于200个并发在线用户，峰值QPS约为10。`),
    heading3("3.3.2 安全性需求"),
    para(`安全性是系统设计的重要考量维度。认证层面采用双Token体系，Access Token与Refresh Token使用不同密钥签名（密钥分离原则），防止单密钥泄露导致全面失陷。Refresh Token Rotation机制确保每次刷新时旧Token立即作废，若检测到已被使用的旧Token被再次提交（重放攻击），系统自动撤销该用户所有活跃会话，强制重新登录。通信安全方面，生产环境所有请求强制HTTPS加密传输。验证码安全方面，采用一次性消费、5分钟有效、60秒冷却的多重防护。输入校验方面，前端过滤XSS脚本字符，后端通过Pydantic进行二次数据校验。Redis操作安全方面，全设备登出使用SCAN增量迭代命令，避免KEYS命令阻塞Redis主线程。`),
    heading3("3.3.3 可用性与兼容性需求"),
    para(`系统需兼容iOS 12.0及以上、Android 8.0及以上操作系统，适配刘海屏与底部指示条（使用CSS safe-area-inset-*属性）。界面设计采用粉白柔色系（背景色#FFF5F7）、卡片圆角（16rpx）、毛玻璃效果等ACG清新视觉风格，所有按钮点击态透明度降至0.85并伴有微缩放动画。系统须在微信小程序原生框架下开发，不得转换为Web App。`),
  ];
}

// Chapter 4: System Design
function buildChapter4() {
  return [
    new Paragraph({ children: [new PageBreak()] }),
    heading1("4 系统设计"),
    heading2("4.1 系统架构设计"),
    para(`本系统采用"单机微服务"架构模式，通过Nginx反向代理实现请求的路由分发，将整个系统划分为接入层、业务层、数据层和辅助层四个逻辑层次。接入层以Nginx作为统一入口网关，根据URL路径前缀（/db/*、/ai/*）将请求精准分发至对应的后端服务，对外仅暴露61000端口，隐藏内部服务的实际端口。业务层包含两个核心无状态服务：数据库服务（mongodb_service，端口21325）负责邮箱验证码登录认证、JWT双Token签发与校验、图片数据CRUD、浏览记录和收藏记录的嵌入式文档管理；AI服务（端口21326）负责代理Dify大模型平台的对话API、文件上传和会话管理。两个服务均以Python FastAPI框架开发，以Uvicorn ASGI服务器进程形式直接运行在宿主机上。`),
    para(`数据层由MongoDB和Redis组成。MongoDB作为主数据库，负责用户信息、图片元数据的持久化存储，浏览记录和收藏记录以嵌入式数组存储于User文档中，利用$push/$pull/$slice原子操作维护。Redis作为缓存与会话存储层，管理Refresh Token会话、邮箱验证码和发送冷却期标记。辅助层包括Docker容器化的Nginx服务和Ngrok内网穿透客户端，为系统提供统一入口和公网HTTPS访问能力。`),
    para(`在架构设计上，系统严格遵循"高内聚、低耦合"原则：前端不直接调用Dify API，必须经由自建AI服务中转（添加API Key鉴权和用户ID映射）；数据库服务仅负责"静态图片资源"的管理，AI服务仅负责"动态对话能力"的代理；浏览和收藏记录嵌入用户文档，避免跨集合查询。`),
    para("[图片占位：E-R图.png]", { align: AlignmentType.CENTER, firstLine: false }),
    emptyPara(),

    heading2("4.2 数据库设计"),
    para(`本系统采用MongoDB作为数据库，遵循"面向访问模式设计"（Access Pattern-Oriented）的设计哲学，数据模型围绕应用程序的实际查询模式进行优化。`),
    heading3("4.2.1 概念数据模型（E-R模型）"),
    para(`系统包含两个核心实体：用户（User）和图片（Image）。用户实体具有唯一标识、邮箱、用户名、创建时间、更新时间等属性；图片实体以时间戳作为主键，具有URL、类型（jpg/png/webp/gif）、创建时间等属性。实体之间存在两种多对多关系：浏览关系（Browse）和收藏关系（Favorite），均为用户与图片之间的m:n关联。在物理实现上，这两种关系均采用嵌入式文档模式存储于User文档中，而非创建独立的关联集合。`),
    heading3("4.2.2 物理数据模型"),
    para(`users集合以MongoDB自动生成的ObjectId作为代理主键（应用层转为字符串id），email字段建立唯一索引用于登录查找，username字段建立普通索引。browse_records字段为嵌入式BrowseItem子文档数组，最多保留1000条记录，按image_id降序排列（新的在前），使用$push+$each+$sort+$slice:-1000自动维护和裁剪。favorite_records字段为嵌入式FavoriteItem子文档数组，无上限，按image_id降序排列，添加时先$pull（去重）再$push+$sort保证幂等性。两个子文档均冗余存储image_url字段，查询历史列表时无需再JOIN查询images集合，显著提升读取性能。`),
    para(`images集合以时间戳字符串（格式如"20250610120000"）作为主键，利于按时间排序和追溯。url字段建立唯一索引防止重复入库，type字段建立普通索引支持按图片格式筛选，created_at字段建立降序索引支持最新图片列表查询。前端通过GET /images接口按topic参数和skip/limit分页参数获取图片列表，后端根据type字段匹配对应主题分类。`),
    para(`在Redis中，Refresh Token会话以Key格式"refresh:{user_id}:{jti}"存储，Value为简单标记"1"，TTL与Refresh Token JWT过期时间一致（30天）。邮箱验证码以Key格式"email_code:{email}"存储，TTL为300秒（5分钟）。发送冷却期标记以Key格式"email_cooldown:{email}"存储，TTL为60秒。三种Key各自独立管理生命周期，互不影响。`),
  ];
}

// Chapter 4 continued: API and interface design
function buildChapter4Continued() {
  return [
    heading2("4.3 API接口设计"),
    para(`系统API设计遵循RESTful风格，采用统一的JSON响应格式：{"code": 200, "msg": "success", "data": {...}}。数据库服务（/db/*）和AI服务（/ai/*）的所有API均通过Nginx反向代理统一对外暴露。`),
    heading3("4.3.1 数据库服务API"),
    para(`数据库服务（端口21325）负责处理用户认证与业务数据的全部API。认证相关端点包括：POST /auth/send-code（发送邮箱验证码，60秒冷却）、POST /auth/login（验证码校验+自动注册+签发双Token）、POST /auth/refresh（Token轮换刷新+重放检测）、POST /auth/logout（单设备或全设备登出）、GET /auth/me（获取当前用户信息）。业务数据端点包括：POST /browse/（批量记录浏览）、GET /browse/?limit=&skip=（分页查询浏览记录）、DELETE /browse/（清空浏览记录）、POST /favorite/（添加收藏，幂等设计）、GET /favorite/?limit=&skip=（分页查询收藏记录）、DELETE /favorite/{image_id}（取消单条收藏）、DELETE /favorite/（清空全部收藏）。所有业务API（除认证入口外）均要求在Header中携带Authorization: Bearer <access_token>，由FastAPI的Depends依赖注入中间件统一拦截校验。`),
    heading3("4.3.2 AI服务API"),
    para(`AI服务（端口21326）通过Nginx /ai/*路径代理Dify对话型应用的Service API。核心端点包括：POST /ai/v1/chat-messages（发送对话消息，支持SSE流式输出，通过enableChunked参数启用分块传输）、POST /ai/v1/files/upload（上传图片文件供多模态分析，multipart/form-data格式）、GET /ai/v1/conversations（获取用户会话列表，按更新时间倒序）、GET /ai/v1/messages（获取会话历史消息，倒序返回需前端反转）、DELETE /ai/v1/conversations/{id}（删除会话）、POST /ai/v1/chat-messages/{task_id}/stop（停止流式响应）、POST /ai/v1/messages/{message_id}/feedbacks（消息反馈评价）。所有AI相关请求的user参数必须通过数据库服务的GET /auth/me获取真实用户ID，不得使用前端传入值，确保用户会话隔离和安全性。`),
    heading3("4.3.3 前端请求拦截器"),
    para(`小程序前端通过utils/request.js封装了统一的请求拦截器，所有业务请求均经由该拦截器处理。其核心功能包括：自动在请求Header中添加Authorization: Bearer <access_token>；检测401响应并自动触发Token刷新（POST /auth/refresh）；全局刷新锁（isRefreshing）+请求等待队列（refreshQueue）机制确保同一时刻只有一个刷新请求在执行，其余401请求排队等待结果；刷新成功后自动用新Token重试队列中所有请求；刷新失败（如Refresh Token也过期或检测到重放攻击）则清除本地Token并跳转登录页；支持skipAuth参数以跳过认证（仅用于发送验证码、登录等入口接口）。该拦截器同时支持Promise风格（.then/.catch）和传统回调风格（success/fail），业务代码无需关心Token的刷新细节。`),
  ];
}

// Chapter 5: Implementation
function buildChapter5() {
  return [
    new Paragraph({ children: [new PageBreak()] }),
    heading1("5 系统实现"),
    heading2("5.1 用户认证模块实现"),
    heading3("5.1.1 登录界面"),
    para(`登录页面作为小程序的入口界面，在用户未登录时首先展示。页面设计简洁明了，包含邮箱输入框、验证码输入框、发送验证码按钮和登录按钮。用户首次输入邮箱并获取验证码即自动完成注册。界面采用粉白柔色系背景，输入框使用圆角卡片风格，按钮具有点击态透明度变化与微缩放动画效果。`),
    para("[图片占位：项目展示图/登陆界界面.png]", { align: AlignmentType.CENTER, firstLine: false }),
    emptyPara(),
    heading3("5.1.2 邮箱验证码登录"),
    para(`邮箱验证码登录功能的实现涉及前后端多个模块的协同工作。用户在前端登录页输入邮箱地址后点击"发送验证码"，前端调用POST /auth/send-code接口。后端verification.py模块的send_code函数按以下流程编排：首先通过check_send_cooldown检查Redis中是否存在email_cooldown:{email}键（60秒冷却期），若存在则返回HTTP 429并提示剩余等待秒数；然后调用generate_code使用random.choices生成6位数字验证码；接着save_verification_code将验证码存入Redis（email_code:{email}，TTL 300秒）；随后调用utils/message_util.py通过QQ邮箱SMTP服务（smtp.qq.com:465，SSL加密）发送包含验证码的HTML格式邮件；最后set_send_cooldown设置60秒冷却标记。验证码校验由verify_and_consume_code函数完成：从Redis读取验证码并比对，匹配成功后立即DEL删除该Key（一次性消费），防止同一验证码被重复利用。`),
    heading3("5.1.2 JWT双Token认证体系"),
    para(`登录验证通过后，router.py的登录处理逻辑首先通过MongoDB查找用户，不存在则自动创建新用户（验证码即注册），随后调用_issue_tokens函数签发双Token。jwt.py模块负责Token的创建与校验：create_access_token和create_refresh_token函数分别使用不同的环境变量密钥（ACCESS_TOKEN_SECRET_KEY和REFRESH_TOKEN_SECRET_KEY）对载荷进行HS256签名。载荷包含iss（签发者）、sub（用户MongoDB ObjectId）、jti（UUID4唯一标识）、type（access/refresh，防互换攻击）、iat（签发时间）、nbf（生效时间）、exp（过期时间）七个标准字段，不包含email等业务信息。session_service.py模块负责Refresh Token的Redis会话管理：save_refresh_token在登录/刷新时将jti存入Redis（Key格式refresh:{user_id}:{jti}，TTL与JWT一致）；rotate_refresh_token在Token轮换时原子的删除旧jti并创建新jti；重放检测通过exists_refresh_token判断旧Token是否仍存在于Redis中——若正常刷新后旧Token已被删除，当检测到旧Token被再次提交（可能是攻击者截获Token后使用），系统调用revoke_all_user_tokens使用SCAN增量迭代撤销该用户所有活跃会话。`),
    heading3("5.1.3 前端Token无感刷新"),
    para(`前端请求拦截器（utils/request.js）实现了完整的Token无感刷新机制。当API请求返回401状态码且响应头X-Token-Error为"expired"时，拦截器自动触发刷新流程。全局刷新锁isRefreshing确保同一时刻只有一个POST /auth/refresh请求在执行——首个401请求触发刷新并将isRefreshing置为true，后续并发401请求检测到刷新进行中，仅将其resolve/reject回调推入refreshQueue等待队列。刷新成功后调用retryQueue取出队列中所有请求，用新Token替换Authorization头后重新发起；刷新失败则调用failQueue拒绝队列中所有请求，并清除本地Token跳转登录页。该机制实现了用户对Token过期完全无感知的使用体验。`),
  ];
}

function buildChapter5Continued() {
  return [
    heading2("5.2 图片展示与收藏模块实现"),
    heading3("5.2.1 主题分类图片浏览"),
    para(`用户从首页点击主题卡片后，通过URL参数（?code={topic}）传递主题代码至图片鉴赏页。鉴赏页的onLoad生命周期函数接收参数后，调用后端GET /images接口（携带topic和skip/limit分页参数）获取对应分类的图片列表。后端根据type字段匹配图片集合，返回缩略图URL、图片ID等字段。前端以两列网格布局展示缩略图，使用scroll-view组件的bindscrolltolower事件监听滚动到底部，自动递增skip参数加载下一页。缩略图尺寸统一为宽度400px并保持原始比例，已由管理员通过导入脚本批量预裁剪。首页展示了十余种主题分类入口（PC壁纸、AI生成图、风景、萌图、原神等），每个主题以卡片形式呈现图标和名称。`),
    para("[图片占位：项目展示图/首页.png]", { align: AlignmentType.CENTER, firstLine: false }),
    emptyPara(),
    heading3("5.2.2 图片详情弹窗与收藏管理"),
    para(`用户点击网格中的缩略图后，前端获取该图片的完整信息（原图URL、AI描述、标签、收藏状态）并在模态窗口中展示。收藏操作调用POST /favorite/接口，后端采用$pull（按image_id先删除旧记录）+$push（追加新记录）+$sort（降序排列）的原子操作序列实现幂等添加，确保同一用户对同一图片不会出现重复收藏。取消收藏调用DELETE /favorite/{image_id}，使用$pull操作匹配并删除。收藏操作触发微信小程序wx.vibrateShort({type: 'light'})实现轻量级震动反馈，同时toast提示操作结果。浏览记录在用户查看图片详情时自动批量提交至POST /browse/接口，后端使用$push+$each+$sort+$slice:-1000维护最新的1000条记录。`),

    heading2("5.3 AI智能对话模块实现"),
    heading3("5.3.1 SSE流式对话"),
    para(`AI对话模块是本系统技术实现的核心难点与亮点。用户在前端搜索页输入文字或有选择地上传图片后点击发送，前端首先判断是否有图片附件——若有则先调用POST /ai/v1/files/upload（multipart/form-data格式）将图片上传至Dify临时存储并获取upload_file_id。随后构造对话请求体（包含query、user、conversation_id、files数组、response_mode:"streaming"）发送至POST /ai/v1/chat-messages，并设置enableChunked:true启用分块传输。前端通过wx.request的onChunkReceived回调实时接收SSE事件流（注意该回调在微信开发者工具模拟器中不可用，需真机测试），解析事件类型：message事件提取answer字段逐Token追加显示，实现打字机效果；message_end事件标记流式完成并保存conversation_id和message_id；agent_thought事件（Agent模式）拼接思考过程；error事件显示错误信息。`),
    para("[图片占位：项目展示图/探索.png]", { align: AlignmentType.CENTER, firstLine: false }),
    emptyPara(),
    heading3("5.3.2 会话管理与思考过程展示"),
    para(`侧边栏会话列表通过GET /ai/v1/conversations接口获取，按updated_at倒序排列，支持分页加载。点击某会话调用GET /ai/v1/messages获取历史消息（API以倒序返回，前端需reverse反转为正序显示），用户消息与AI回复交替排列。左滑删除调用DELETE /ai/v1/conversations/{id}。新建对话按钮清空当前conversation_id，下次发送消息时自动创建新会话。AI回复中的思考过程（<think>...</think>标签内容或Agent模式的agent_thought事件）被实时剥离至thought字段，默认以灰色胶囊按钮"▸ 💭 思考过程"折叠展示，用户点击后展开为灰色代码风格文本块（max-height: 400rpx，超出可滚动），思考内容可选中复制。`),
    heading3("5.3.3 AI聊天输入区域实现"),
    para(`底部AI输入区域采用了经过多次迭代优化的Flex布局方案。核心布局结构为：根容器chat-page设置height:100vh和display:flex，chat-main主区域设置flex:1、display:flex、flex-direction:column、min-height:0（关键：允许收缩）。消息滚动区message-scroll设置flex:1 1 0（可缩至零）和min-height:0（允许低于内容高度）。底部输入区footer-area设置flex-shrink:0（不可压缩），并设置padding-bottom包含env(safe-area-inset-bottom)适配全面屏。当上传图片预览行撑高footer-area时，message-scroll自动收缩让位，实现底部锚定不动、向上生长的效果。输入框使用textarea组件并设置auto-height="{{true}}"实现1至4行的自然增长，CSS max-height:208rpx封顶后内容区自动滚动。该方案解决了微信小程序中底部输入区域的五个经典坑点：底部间距不足、上传按钮对齐问题、输入框高度不随行数增长、添加图片后底部溢出屏幕、overflow:hidden裁剪页面内容。`),

    heading2("5.4 用户设置与个人中心"),
    para(`用户设置页（"我的"Tab页面）展示当前登录用户的基本信息（邮箱、用户名），并提供浏览记录、我的收藏、退出登录等功能的入口。浏览记录以列表形式分页展示用户近期浏览过的图片，按时间倒序排列，最多保留1000条，支持分页加载。收藏列表以图片网格形式展示用户收藏的图片，支持在前端直接取消收藏（点击取消按钮即时更新UI并调DELETE接口），空收藏时显示"还没有收藏任何图片"的提示。退出登录功能设有二次确认弹窗，确认后调用POST /auth/logout撤销当前Refresh Token，清除本地存储的所有Token，并跳转至登录页。重新登录后，之前的收藏和浏览数据完整保留。`),
    para("[图片占位：项目展示图/个人中心.png]", { align: AlignmentType.CENTER, firstLine: false }),
    emptyPara(),

    heading2("5.5 合规性页面"),
    para(`本系统实现了独立的用户协议展示页面和隐私政策展示页面。用户协议页面采用萌系二次元ACG风格设计，以柔和渐变背景（粉白到淡紫）、毛玻璃半透明磨砂质感卡片包裹协议文本，标题栏显示"用户协议"并提供返回按钮，协议文本支持纵向滚动查看。隐私政策页面展示了开发者处理的信息类型（邮箱用于登录与跨平台同步、剪切板用于文本粘贴与复制、相册写入权限用于保存图片、选中的照片用于AI多模态分析），以及第三方SDK使用情况（本小程序未使用任何第三方插件或SDK）、用户权益（查阅、复制、更正、删除等法定权利）、信息存储位置（中国大陆）等内容。`),
    para("[图片占位：项目展示图/用户协议.png]", { align: AlignmentType.CENTER, firstLine: false }),
    emptyPara(),
    para("[图片占位：项目展示图/隐私协议.png]", { align: AlignmentType.CENTER, firstLine: false }),
    emptyPara(),
  ];
}

// Chapter 6: Testing & Deployment
function buildChapter6() {
  return [
    new Paragraph({ children: [new PageBreak()] }),
    heading1("6 测试、部署与上线审核"),
    heading2("6.1 开发环境与工具链"),
    para(`系统开发环境基于Windows 11操作系统，使用微信开发者工具进行小程序前端开发与调试，Visual Studio Code作为后端代码编辑器。Python版本为3.14及以上，MongoDB和Redis均以单实例模式运行在本地宿主机。Nginx通过Docker Compose进行容器化部署（nginx:stable-alpine镜像），Ngrok客户端建立内网穿透隧道。后端依赖管理使用pyproject.toml配置文件。开发阶段可在微信开发者工具中勾选"不校验合法域名"选项绕过域名限制，方便本地调试。`),

    heading2("6.2 部署方案"),
    para(`系统部署分为以下步骤：首先在本地主机安装Python 3.14+、MongoDB和Redis，并通过pip安装项目依赖；然后从.env.example复制环境变量配置文件并填写所有敏感凭证（MongoDB连接字符串、Redis密码、QQ邮箱SMTP授权码、JWT签名密钥对、Dify API Key等）；接着使用docker-compose up启动Nginx容器（内部8000端口映射至宿主机61000）；随后分别启动数据库服务（python main.py，Uvicorn监听0.0.0.0:21325）和AI服务（独立项目，端口21326）；再运行ngrok客户端将本地61000端口映射至公网HTTPS地址（如https://scraggly-regress-cape.ngrok-free.dev）；最后将Ngrok提供的公网域名配置为微信小程序后台的合法request/socket/uploadFile/downloadFile域名，完成前后端联调。系统的合法域名列表已预先规划了多种AI服务提供商的域名（如api.openai.com、api.deepseek.com、api.anthropic.com等共计20个request合法域名），为后续扩展预留了空间。`),

    heading2("6.3 上线审核过程"),
    para(`微信小程序上线审核是本项目面临的重要挑战之一。在首次提交审核时，系统因涉及AI生成内容功能，被平台判定为"高价值产物"，不符合个体开发者资质要求，审核被驳回。第二次审核尝试同样因相同原因被驳回。经与业内资深开发者交流后了解到，微信小程序平台当前对涉及AI内容的个体开发者审核策略较为严格，凡包含大模型对话、AI生成等功能的个体开发者提交，均可能被归类为需要企业资质的高价值应用。针对这一问题，可行的解决方案包括：将AI对话界面在审核期间调整为模拟的"好友聊天"风格界面，弱化AI属性感知；或将AI功能模块暂时隐藏，待审核通过后再通过后端配置开关启用。这一经历也为类似含AI功能的小程序开发者提供了重要的审核实践经验参考。`),
    para("[图片占位：服务上线审核记录/第一次审核打回.png]", { align: AlignmentType.CENTER, firstLine: false }),
    emptyPara(),
    para("[图片占位：服务上线审核记录/第二次审核打回.png]", { align: AlignmentType.CENTER, firstLine: false }),
    emptyPara(),

    heading2("6.4 开发过程中的典型问题与解决方案"),
    para(`在系统开发过程中，积累了一系列具有代表性的技术问题及其解决方案。在微信开发者工具方面，工具内置的"代码质量"静态分析模块存在一个已知的逻辑缺陷Bug：将components/navigation-bar/navigation-bar.json错误地归类为"无使用的组件"并建议删除。然而该组件的引用关系在依赖图中明确显示为正确（app.json→home页面→navigation-bar组件）。实际上，工具的静态扫描器与依赖图构建器使用了分离的识别逻辑，扫描器未能正确解析组件JSON中的"component":true声明及其引用关系。解决方式为忽略该误报或通过.eslintignore文件排除该文件的扫描，绝不可删除该JSON文件（否则组件将失效）。`),
    para(`在Redis客户端兼容性方面，redis-py 6.x及以上版本默认使用RESP3协议，会在认证之前发送HELLO命令，导致与部分Redis配置的认证时序冲突而抛出AuthenticationError。解决方案为在Redis客户端初始化时显式设置protocol=2强制使用RESP2协议。在MongoDB驱动迁移方面，长期广泛使用的motor异步驱动已被MongoDB官方弃用，解决方案为切换至pymongo 4.x自带的AsyncMongoClient原生异步接口，并使用Pydantic BaseModel替代Beanie ODM进行数据校验。在Ngrok域名管理方面，Ngrok免费版每次重启会分配新的随机子域名，需要同步更新微信小程序后台的合法域名配置，且每月仅有5次修改机会。解决方案为尽量保持Ngrok会话的持续运行，或升级至付费版获得固定域名。`),
  ];
}

// Chapter 7: Conclusion
function buildChapter7() {
  return [
    new Paragraph({ children: [new PageBreak()] }),
    heading1("7 总结与展望"),
    heading2("7.1 工作总结"),
    para(`本文从软件工程的全生命周期视角，完整阐述了"基于微信小程序的ACG智能图廊系统"的设计与实现过程。在需求分析阶段，明确了项目的核心定位——以ACG图片为核心内容、以多模态AI对话为核心交互的智能图廊，并从功能需求、非功能需求、数据需求等多个维度进行了系统化的需求定义，形成了完整的需求规格说明书（SRS）。在系统设计阶段，采用逻辑分层架构将系统划分为接入层、业务层、数据层和辅助层，基于"高内聚、低耦合"原则完成组件划分与接口约定，并通过嵌入式文档模式优化了MongoDB的数据访问性能。在实现阶段，完成了邮箱验证码登录、JWT双Token认证、主题分类浏览、收藏管理、AI多模态流式对话、会话管理等全部核心功能的前后端开发，并针对微信小程序底部输入区域的布局问题进行了深入的技术攻关。在部署阶段，通过Docker+Nginx+Ngrok的组合方案，实现了从本地开发到公网HTTPS服务的完整链路。`),
    para(`本系统在以下方面具有创新性和技术特色：其一，将传统图片浏览应用与大模型AI对话能力深度融合，实现了"可看、可聊、可思考"的新型交互体验，区别于市面上功能单一的传统图廊应用；其二，采用JWT双Token+Refresh Token Rotation+重放检测的多层安全防护体系，在保持后端无状态设计的同时实现了企业级的安全保障；其三，前端的统一请求拦截器通过全局刷新锁+等待队列机制，实现了Token无感刷新的优雅方案，业务代码零侵入；其四，针对微信小程序flex布局中底部输入区域的系列问题，总结出"flex-shrink:0固定两区+flex:1 1 0可缩消息区+min-height:0关键解锁"的铁律组合，具有较强的通用参考价值。`),

    heading2("7.2 存在的不足"),
    para(`本系统在当前阶段仍存在以下不足之处：前端部分页面（如主题列表的图标展示、浏览记录和收藏列表的UI完善度）尚有提升空间；图片数据目前依赖管理员后台手动导入，缺乏友好的内容管理后台（CMS）；AI服务的自然语言搜索能力尚未与图片数据库的标签和描述进行深度整合，当前AI对话主要依赖Dify平台独立完成，未能充分利用本地的图片元数据；Ngrok免费版的不稳定性和域名变动问题增加了运维负担；系统上线审核因涉及AI内容功能而遇到阻碍，需要探索更可行的审核策略。`),

    heading2("7.3 未来展望"),
    para(`在后续的演进方向上，本系统可以从以下几个维度进行优化和扩展。在高可用性方面，当前的单机部署架构可演进为云原生多副本部署：在Nginx前方增加云负载均衡器（SLB/ALB），使用Kubernetes将数据库服务和AI服务部署为多副本并分布到多台云主机，将MongoDB从单实例升级为副本集架构（1主+2从+1仲裁），将Redis升级为哨兵模式或集群模式保障会话数据高可用。在功能扩展方面，可以引入基于向量检索的图片自然语言搜索引擎，将图片的AI描述和标签进行向量化存储，实现更精准的语义搜索；可以构建内容管理后台（CMS），支持图片的批量导入、标签编辑、数据统计等管理功能；可以增加用户个性化推荐功能，基于浏览和收藏历史推荐相似风格的图片。在安全增强方面，可以将Refresh Token从本地存储迁移至httpOnly Secure SameSite Cookie，增加速率限制、IP绑定和设备指纹等安全机制。在跨平台扩展方面，当前基于邮箱的认证体系天然支持跨平台数据互通，后续可以将AI对话历史、收藏列表等核心数据同步至Web端和移动App端，构建完整的跨端ACG智能图廊生态。`),
  ];
}

// ========================
// BUILD DOCUMENT
// ========================
async function main() {
  // Note: Headers/footers need to be in individual sections due to docx-js compatibility
  // We'll use a simple structure: single section with all content

  const children = [
    // Cover page
    ...buildCoverPage(),

    // Chinese title and abstract
    ...buildChineseTitle(),
    ...buildAbstractCN(),

    // English abstract
    ...buildAbstractEN(),

    // TOC (will show "请更新域" until opened in Word and updated)
    ...buildTOC(),

    // Chapters
    ...buildChapter1(),
    ...buildChapter2(),
    ...buildChapter3(),
    ...buildChapter3Continued(),
    ...buildChapter4(),
    ...buildChapter4Continued(),
    ...buildChapter5(),
    ...buildChapter5Continued(),
    ...buildChapter6(),
    ...buildChapter7(),
  ];

  const doc = new Document({
    styles: {
      default: {
        document: {
          run: {
            font: "Times New Roman",
            eastAsia: "宋体",
            size: 24,
          },
        },
      },
      paragraphStyles: [
        {
          id: "Heading1",
          name: "Heading 1",
          basedOn: "Normal",
          next: "Normal",
          quickFormat: true,
          run: {
            font: "Times New Roman",
            eastAsia: "黑体",
            size: 30,
            bold: true,
          },
          paragraph: {
            spacing: { before: 240, after: 120, line: 360, lineRule: "auto" },
            outlineLevel: 0,
          },
        },
        {
          id: "Heading2",
          name: "Heading 2",
          basedOn: "Normal",
          next: "Normal",
          quickFormat: true,
          run: {
            font: "Times New Roman",
            eastAsia: "黑体",
            size: 28,
            bold: true,
          },
          paragraph: {
            spacing: { before: 200, after: 100, line: 360, lineRule: "auto" },
            outlineLevel: 1,
          },
        },
        {
          id: "Heading3",
          name: "Heading 3",
          basedOn: "Normal",
          next: "Normal",
          quickFormat: true,
          run: {
            font: "Times New Roman",
            eastAsia: "黑体",
            size: 24,
            bold: true,
          },
          paragraph: {
            spacing: { before: 160, after: 80, line: 360, lineRule: "auto" },
            outlineLevel: 2,
          },
        },
      ],
    },
    sections: [
      {
        properties: {
          page: {
            size: {
              width: 11906,  // A4
              height: 16838,
            },
            margin: {
              top: 1440,    // 1 inch = 2.54cm
              bottom: 1440,
              left: 1800,   // slightly wider left for binding
              right: 1440,
            },
          },
        },
        headers: {
          default: new Header({
            children: [
              new Paragraph({
                children: [txt("广东培正学院期末大作业", { font: DEF_FONT, size: 18 })],
                alignment: AlignmentType.CENTER,
              }),
            ],
          }),
        },
        footers: {
          default: new Footer({
            children: [
              new Paragraph({
                children: [
                  txt("第 ", { font: DEF_FONT, size: 18 }),
                  new TextRun({ children: [PageNumber.CURRENT], font: DEF_FONT, size: 18 }),
                  txt(" 页", { font: DEF_FONT, size: 18 }),
                ],
                alignment: AlignmentType.CENTER,
              }),
            ],
          }),
        },
        children,
      },
    ],
  });

  const buffer = await Packer.toBuffer(doc);
  const outPath = "B:/study/微信小程序/期末作业/文档/ACG智能图廊论文_生成稿.docx";
  fs.writeFileSync(outPath, buffer);
  console.log("✅ Document generated: " + outPath);
  console.log("File size: " + (buffer.length / 1024).toFixed(1) + " KB");
}

function buildTOC() {
  return [
    new Paragraph({ children: [new PageBreak()] }),
    new Paragraph({
      children: [txt("目录", { font: HEI_FONT, size: 30, bold: true })],
      alignment: AlignmentType.CENTER,
      spacing: { before: 240, after: 360 }
    }),
    new TableOfContents("目录", {
      hyperlink: true,
      headingStyleRange: "1-3",
    }),
  ];
}

main().catch(err => {
  console.error("Error:", err);
  process.exit(1);
});

<!-- PROCESSED: 2026-05-13 ｜ 系统架构 / API / 数据表 / 流程图全部沉淀到 PROJECTS/work/qiniu-zeroops-rca-agent/system-anatomy.md。INBOX 副本可随时删除。 -->

原型图
1. 首页: 
整体服务状态View
暂时无法在飞书文档外展示此内容
功能描述
- 作为用户我可以观察到服务之间的依赖关系，父节点服务依赖子节点服务
- 作为用户我可以观察到整体服务状态，绿色为服务正常，黄色为有异常AI正在观察和分析，红色为服务有异常。有标记的服务表示有版本灰度发布正在进行中
2. 服务详情页View及子页面View
服务详情页View
暂时无法在飞书文档外展示此内容
功能描述
- 作为用户我可以观察到该服务每个版本
  1. 版本号
  2. 发布状态（正常/异常/正在观察分析异常）
  3. 发布占比
  4. 四个黄金指标的实时数据统计表（延迟/流量/错误/饱和度）
- 作为用户我可以观察到该服务特定版本
  1. 版本号
  2. 发布状态（正常/异常/正在观察分析异常）
  3. 发布占比
  4. 发布已经持续时间
  5. 预计完成时间
  6. 四个黄金指标的实时数据（延迟/流量/错误/饱和度）看板
- 作为用户我可以对服务正在发布的版本进行暂停、继续操作
- 作为用户我可以对服务任何版本进行回滚操作
版本发布View
暂时无法在飞书文档外展示此内容
功能描述
- 作为用户我可以对该服务创建灰度发布，指定发布版本，并可以看到目标版本的修改时间
- 作为用户我可以对该服务创建灰度发布，立即/预定发布时间（准确到分钟）
- 作为用户我不可以同时重复新建灰度发布相同版本（选择目标版本发布时不会显示正在发布的版本）
发布任务计划View
暂时无法在飞书文档外展示此内容
功能描述
- 作为用户我可以对该服务创建灰度发布时自动签名
- 作为用户我可以修改发布时间
- 作为用户我可以取消发布计划
服务指标View
暂时无法在飞书文档外展示此内容
功能描述：
- 作为用户我可以观察到该服务版本四个黄金指标的实时数据统计看板（延迟/流量/错误/饱和度）
3. 系统状态变更记录页View及子页面View
服务变更记录View
暂时无法在飞书文档外展示此内容
功能描述：
- 作为用户我可以观察到哪些服务进行了版本发布，完成了多少，健康状态
- 作为用户我可以观察到服务版本发布每一批次的开始时间、结束时间、健康状态
告警规则变更记录View
暂时无法在飞书文档外展示此内容
功能描述：
- 作为用户我可以观察哪些告警阈值进行了变更，变更了多少，与变更理由
事件日志View（保留参考）
暂时无法在飞书文档外展示此内容
功能描述：
- 作为用户我可以观察到服务版本发布每一批次的详细每一个事件的发生时间、健康状态、事件类型、事件详细数据
- -> AI决策过程

4. 告警记录页View及ai分析页面View
ai分析不要重复解决相同问题
告警是否关联发布服务
告警 触发，判断是否与正在灰度的服务有关
mock系统里需要将告警带上service与version标签
下游服务发布 导致上游异常，收到上游告警，看告警服务的依赖项有没有正在发布
告警记录Vie
[图片]
AI分析处理记录View
如果一轮任务规划没有完成任务，会根据上文信息进行新一轮plan，生成新的plan列表
暂时无法在飞书文档外展示此内容

[图片]

[图片]
API定义
1. 服务信息接口
1.1 获取所有服务列表
  请求
GET /v1/services
  响应
{
    "items": {
        {
            "name": "stg", // 服务名称
            "deployState": "InDeploying", // 发布状态：InDeploying|AllDeployFinish
            "health": "Normal", // 健康状态：Normal/Processing/Error
            "deps": ["stg","meta","mq"]
        },
        {
            "name": "meta", // 服务名称
            "deployState": "InDeploying", // 服务发布状态：InDeploying|AllDeployFinish
            "health": "Normal"  // 服务健康状态：Normal/Warning/Error
            "deps": []
        },
    }
}
1.2 获取服务详情
  请求：
GET /v1/services/:service/activeVersions
  响应：
{
    "items": [
        {
            "version": "v1.0.1",
            "deployID": "1001", 
            "startTime": "2024-01-01T00:00:00Z", // 开始时间
            "estimatedCompletionTime": "2024-01-01T03:00:00Z", // 预估完成时间
            "instances": 10 // 实例个数（比例由所有items的instance加起来做除法)
            "health": "Normal" // 健康状态：Normal/Warning/Error
        }
    ]
}
1.3 获取可用服务版本（已发布的排除）
  请求：
GET /v1/services/:service/availableVersions
  指定服务的可用版本包。接口只返回所有未发布的版本包列表，已发布的版本包不下发。
  响应：
{
    "items": {
        {
            "version": "v1.0.1", // 版本包对应的版本号
            "createTime": "2024-01-01T03:00:00Z" // 版本包创建时间，RFC3339 格式
        },
        {
            "version": "v1.0.2",
            "createTime": "2024-01-02T03:00:00Z"
        }
    }
}
2. 发布任务接口
2.1 新建发布任务
  请求：
POST /v1/deployments

{
    "service": "stg"
    "version": "v1.0.1", // 版本包对应的版本号
    "schedueTime": "2024-01-02T04:00:00Z" // 可选参数，不填为立即发布
}
  接口只返回所有未发布的版本包列表，已发布的版本包不下发。
  响应：// 同一个版本拒绝多次发布
{
    "id": "1001" // 发布id
}
  错误码：
  - 409: AlreadyInDeployment
2.2 获取待发布计划列表
  请求：
GET /v1/deployments?type=Schedule&service=stg  // InDeployment/Schedule/Finished
  获取某个服务的所有未开始的发布任务列表。接口只返回所有未开始/进行中的发布任务列表，已发布的不包含在列表中
  响应：
{
    "items": {
        {
            "id": "1001",
            "service": "stg",
            "version": "v1.0.1",
            "status": "InDeployment",
            "scheduleTime": "" // 已经发了
        },
        {
            "id": "1002",
            "service": "stg",
            "version": "v1.0.2",
            "status": "InDeployment",
            "scheduleTime": "2024-01-03T05:00:00Z"
        },
        {
            "id": "1003",
            "service": "stg",
            "version": "v1.0.3",
            "status": "InDeployment",
            "finishTime": "2024-01-03T05:00:00Z"
        },
        {
            "id": "1003",
            "service": "stg",
            "version": "v1.0.3",
            "status": "rollbacked",
            "finishTime": "2024-01-03T05:00:00Z"
        }
    }
}
2.3 修改未开始的发布任务
  请求：
POST /v1/deployments/:deployID
{
    "version": "v1.0.2",
    "scheduleTime": "2024-01-03T06:00:00Z" // 新的计划发布时间（当前只能修改此字段）
}
  只能修改还未开始的发布任务
  响应：无响应体。200状态码，或异常码
2.4 删除未开始的发布任务
  发布任务未开始的可以直接删除，否则只能暂停或终止
  请求：
DELETE /v1/deployments/:deployID
  注释：只能删除计划中的发布。已完成、进行中的都不能删除。
  响应：无响应体。200状态码，或异常码
2.5 暂停正在灰度的发布任务
  请求：
POST /v1/deployments/:deployID/pause
  暂停发布任务。只能处理已经开始灰度，且未完成100%灰度的发布任务
  响应：无响应体。200状态码，或异常码
2.6 继续发布
POST /v1/deployments/:deployID/continue
  响应：无响应体。200状态码，或异常码
2.7 回滚发布任务
  请求：
POST /v1/deployments/:deployID/rollback
  回滚发布任务，它会将此版本已灰度的实例回滚至上一个版本，即使是已完成的发布也能回滚。
  响应：无响应体。200状态码，或异常码
3. 服务指标接口
3.1 获取服务metrics指标值
  请求：
GET /v1/metricStats/:service
  version对应的状态，通过“获取服务详情”接口获取，前端根据verion进行
  响应：
{
    "summary": { // 所有实例的聚合值
        "metrics": [ // 此版本发布的metric指标内容
            {
                "name": "latency",
                "value": 10 // 单位: ms
            },
            {
                "name": "traffic", // 流量
                "value": 1000 // Qps
            },
            {
                "name": "errorRatio", // 错误率
                "value": 10 
            },
            {
                "name": "saturation", // 饱和度
                "value": 50 // 百分比
            }
        ]
    }
    "items": [
        {
            "version": "v1.0.1",
            "metrics": [ // 此版本发布的metric指标内容
                {
                    "name": "latency",
                    "value": 10 // 单位: ms
                },
                {
                    "name": "traffic", // 流量
                    "value": 1000 // Qps
                },
                {
                    "name": "errorRatio", // 错误率
                    "value": 10 
                },
                {
                    "name": "saturation", // 饱和度
                    "value": 50 // 百分比
                }
            ]
        }
    ]
}
3.2 获取服务指标数据
  请求：
GET /v1/metrics/:service/:name?version=v1.0.1&start=2024-01-03T06:00:00Z&end=2024-01-03T06:00:00Z&granule=5m(1m/1h)
  按对齐后的时间返回。如果没有指定version，则取的是所有实例的聚合。
  :name由“获取服务metrics指标值”接口返回的指标列表指定。
  响应：
// 参考 Prometheus query_range 返回结构体。参考链接：https://prometheus.io/docs/prometheus/latest/querying/api/

{
   "status" : "success",
   "data" : {
      "resultType" : "matrix",
      "result" : [
         {
            "metric" : {
               "__name__" : "up",
               "job" : "prometheus",
               "instance" : "localhost:9090"
            },
            "values" : [
               [ 1435781430.781, "1" ],
               [ 1435781445.781, "1" ],
               [ 1435781460.781, "1" ]
            ]
         },
         {
            "metric" : {
               "__name__" : "up",
               "job" : "node",
               "instance" : "localhost:9091"
            },
            "values" : [
               [ 1435781430.781, "0" ],
               [ 1435781445.781, "0" ],
               [ 1435781460.781, "1" ]
            ]
         }
      ]
   }
}
4. 告警事件接口
4.1 获取告警事件列表
  请求：
GET /v1/issues?start=xxxx&limit=10
// 可带额外一个query条件state=Closed，不传表示查询所有
  响应：
{
    "items": [ 
        {
            "id": "xxx", // 告警 issue ID
            "state": "Closed", // 告警条目的状态。Closed处理完成、Open处理中
            "level": "P0", // 枚举值：P0严重、P1重要、P2、Warning需要关注但不是线上异常
            "alertState": "Restored", // 告警处理状态。Pending待处理，Restored 已恢复、AutoRestored 系统自动恢复、InProcessing 处理中
            "title": "yzh S3APIV2s3apiv2.putobject 0_64K上传响应时间95值:50012ms > 450ms", // 告警标题
            "labels": [
                {
                    "key": "api",
                    "value: "s3apiv2.putobject"
                },
                {
                    "key": "idc",
                    "value": "yzh"
                }
            ],
            "alertSince": "2025-05-05 11:00:00.0000Z"
            "resolved_at": "" // 告警已恢复, 记录恢复时间
        }
    ],
    "next": "xxxx"
}
4.2 获取某一个告警的处理
  请求：
GET /v1/issues/:issueID
  响应：
{
    "id": "xxx", // 告警 issue ID
    "state": "Closed", // 告警条目的状态。Closed处理完成、Open处理中
    "level": "P0", // 枚举值：P0严重、P1重要、P2、Warning需要关注但不是线上异常
    "alertState": "Restored", // 告警处理状态。
        // Pending 待处理、Restored 已恢复、AutoRestored 系统自动恢复、InProcessing 处理中
    "title": "yzh S3APIV2s3apiv2.putobject 0_64K上传响应时间95值:50012ms > 450ms", // 告警标题
    "labels": [
        {
            "key": "api",
            "value": "s3apiv2.putobject"
        },
        {
            "key": "idc",
            "value": "yzh"
        }
    ],
    "alertSince": "2025-05-05 11:00:00.0000Z",
    "comments": [
        {
            "createdAt": "2024-01-03T03:00:00Z",
            "content": "markdown content" // 里面为一个整体的markdown，记录了AI的行为
        },
    ],

5. 系统变更接口
5.1 获取服务变更记录
  请求：
GET /v1/changelog/deployment?start=xxxx&limit=10
  从最新的变更记录往前排序。
  响应：
{
    "items": [
       {
        "serivce": "stg",
        "version": "v1.0.1", // 版本发布id
        "startTime": "2024-01-03T03:00:00Z",
        "endTime": "2024-01-03T06:00:00Z", // 可选参数
        "instances": 50, // 灰度实例个数
        "totalInstances": 100, // 灰度时，总实例个数
        "health": "Normal", // 健康状态：Normal/Warning/Error
      }
    ],
    "next": "xxxx"
}
5.2 获取告警变更记录
  请求：
GET /v1/changelog/alertrules?start=xxxx&limit=10
  响应：
// 需要参考promethues的rule修改结构
{
    "items": [
        {
            "name": "http_request_latency_p98_seconds_P1", // 统一化告警规则的名称 
            "editTime": "2024-01-03T03:00:00Z",
            "scope": "", // 空代表修改所有服务；指定了服务名代表修改指定服务；指定了service+service_version代表修改了指定服务版本；
            "values": [
                {
                    "name": "threshold",
                    "old": "10", // 允许是数字字符串，也可以是其它字符串
                    "new": "15"
                }
            ],
            "reason": "xxx", // AI生成的reason
        }
    ],
    "next": "xxxx"
}
  这里面有继承概念：如果某个服务，它有配置，则用自己的规则；如果没有配置，使用默认统一的规则。
  版本tag重要，需要指定
表结构
https://ycn483kz4a5u.feishu.cn/sync/S4modH0Ocs901UbYOsccdKZQnqb
查询
1. 查询某个服务的所有发布任务及对应发布状态
- 涉及表：service、service_deploy_task
- 说明：通过 service.id 与 service_deploy_task.service_id 关联，可获取指定服务的所有发布任务记录，包括任务创建者、发布开始 / 结束时间、发布状态等信息。
2. 查询某个发布任务下的所有发布批次及批次详情
- 涉及表：service_deploy_task、deploy_batch
- 说明：利用 service_deploy_task.id 和 deploy_batch.deploy_id 关联，能得到该发布任务下各批次的开始 / 结束时间、目标发布比例、实际发布节点列表等批次相关信息。
3. 查询某个服务版本的异常状态信息
- 涉及表：service_version、service_state
- 说明：通过 service_version.id 与 service_state.version_id 关联，可查询到该服务版本对应的异常级别、详细信息、报告时间、解决时间以及健康状态等异常相关数据。
4. 查询某个发布批次实际发布的节点及节点对应的服务版本
- 涉及表：deploy_batch、service_node
- 说明：依据 deploy_batch.node_ids与 service_node.node_id 关联，能获取到该发布批次实际发布的节点，以及这些节点对应的服务版本等信息。
5. 查询某个服务的所有版本及其创建时间
- 涉及表：service（服务基础信息）、service_version（服务版本）
- 说明：通过 service.id 和 service_version.service_id 关联，可列出指定服务的所有版本以及各版本的创建时间
6. 查询某个发布任务的所有操作日志
- 涉及表：service_deploy_task、event_logs
- 说明：通过 service_deploy_task.correlation_id 与 event_logs.correlation_id 关联，可获取指定发布任务的所有操作日志记录，包括事件类型、事件详情、操作人、发生时间等信息。
7. 查询某个服务异常的所有告警日志
- 涉及表：alert_issues、alert_issue_comments
- 说明：通过 alert_issues.id 与 alert_issue_comments.issue_id 关联，可获取指定服务异常的所有告警日志记录，包括告警状态、告警分级、告警评论等信息。
架构图
flowchart TB

classDef normal fill:#eef3fb,stroke:#000,stroke-width:1.5px,color:#222;
classDef ai fill:#ffe1e1,stroke:#000,stroke-width:1.5px,color:#222;
classDef external fill:#fff2cc,stroke:#000,stroke-width:1.5px,color:#222;

%% ===================== View 层 =====================
subgraph L1["View层"]
direction LR
    V1[整体服务状态View]
    V2[服务详情页View及子页面View]
    V3[发布任务管理及子页面View]
    V4[系统状态变更记录页View及子页面View]
    V5[事件详情日志View]
end

%% ===================== Controller 层 =====================
subgraph L2["Controller层"]
direction LR
    C1["服务状态<br/>1. 服务列表<br/>2. 服务详情<br/>3. 服务指标<br/>4. 服务状态"]

    C2["发布任务管理<br/>1. 发布任务获取与管理<br/>2. 可用版本信息获取"]

    C3["系统变更<br/>1. 服务变更记录获取<br/>2. 告警变更记录获取"]

    C4[事件详情日志获取]
end

%% ===================== 应用层 =====================
subgraph L3["Model层 / 应用层"]
direction LR
    M1["服务管理模块<br/>1. 服务实例和版本管理<br/>a. 服务发布状态获取<br/>b. 服务详情获取<br/>2. 服务发布管理<br/>a. 制定灰度策略<br/>b. 暂停/取消控制<br/>c. 服务发布执行"]

    M2["监控/告警处理模块<br/>1. 告警接收与处理<br/>2. 服务监控/告警metadata<br/>3. 告警规则调整<br/>4. 周期运行体检<br/>5. 告警等级计算<br/>6. 治愈行为处理"]

    M3[event_log记录模块]
end

%% ===================== 指标分析层 =====================
subgraph L4["指标分析层"]
direction LR
    A1["指标下钻分析（AI）<br/>下钻指标规则<br/>告警规则合理性决策<br/>指标分析结果综合<br/>异常指标分析调用"]

    A2["异常指标分析<br/>数字模型分析<br/>AI大模型分析<br/>指标/日志数据获取Tools"]
end

%% ===================== 基础设施层 =====================
subgraph L5["基础设施层"]
direction LR
    I1["发布系统Adapter<br/>1. 发布行为接口调用<br/>2. 发布阶段信息获取<br/>3. 服务信息获取<br/>4. 服务可选发布包信息获取"]

    I2["Prometheus & 监控系统Adapter<br/>1. 指标数据查询<br/>2. 告警事件接收<br/>3. 告警规则调整"]

    I3[日志查询]
end

%% ===================== 外部系统 =====================
subgraph L6["外部系统 / Mock环境"]
direction LR
    E1[发布系统]
    E2["prometheus环境<br/>& 告警规则配置系统"]
    E3[Mock运行环境]
end

%% ===================== 主调用链路 =====================
V1 -.-> C1
V2 -.-> C1
V3 -.-> C2
V4 -.-> C3
V5 -.-> C4

C1 -.-> M1
C2 -.-> M2
C3 -.-> M2
C4 -.-> M3

M1 -.-> I1
M2 -.-> I2
M2 -.-> A1
M3 -.-> I3

A1 -.-> A2
A2 -.-> I2
A2 -.-> I3

I1 --> E1
I2 --> E2
I3 --> E3

%% ===================== 样式 =====================
class V1,V2,V3,V4,V5,C1,C2,C3,C4,M1,M2,M3,A2,I1,I2,I3 normal;
class A1 ai;
class E1,E2,E3 external;

暂时无法在飞书文档外展示此内容
模块调用关系
Web层
调用模块
被调用模块
说明
Web层-整体服务状态
Controller层-服务状态
收集系统各服务运行状态，在前端界面宏观展示各服务运行情况
Web层-整体服务状态
Controller层-服务状态
收集系统各服务详细信息，在前端界面展示具体某一服务的详细信息
Web层-发布任务管理及其子页面
Controller层-发布任务管理
获取系统中全部的发布任务和可用服务版本，供用户在前端查看发布任务的执行过程，或选择某一版本的服务创建新的发布任务
Web层-系统变更记录及其子页面
Controller层-系统变更
获取变更记录，变更行为包括服务版本变更和告警阈值变更
Web层-事件详情日志
Controller层-事件详情日志获取
获取日志详情，用户可在界面中查看每一次事件的处理记录
Controller层
调用模块
被调用模块
说明
Controller层-服务状态
应用层-服务信息获取
获取系统中各服务的详细信息，包括服务列表、服务状态、服务详情、服务指标、服务状态
Controller层-发布任务管理
应用层-发布任务管理与执行
在新建发布任务场景下，负责制定灰度策略、选择监控指标、生成发布计划；在发布管理场景下，获取各阶段发布信息，并提供暂停/取消控制功能
Controller层-事件详情日志获取
应用层-event_log记录
获取变更记录，变更行为包括服务版本变更和告警阈值变更
应用层
调用模块
被调用模块
说明
应用层-服务信息获取
基础设施层-发布系统Adapter
获取系统中的服务信息数据
应用层-发布任务管理与执行
基础设施层-发布系统Adapter
调用发布行为接口，获取系统中的发布信息数据
应用层-告警接收与处理
基础设施层-Prometheus&监控系统Adapter
持续监听监控系统发出的告警信息
应用层-告警接收与处理
指标分析层-指标下钻分析（AI）
调用AI对告警进行分析，并执行后续处理（故障自愈、告警规则调整）
应用层-告警接收与处理
应用层-event_log记录
记录本次事件发生和全部的处理过程
应用层-治愈行为处理
应用层-event_log记录
记录治愈行为的决策和执行过程
应用层-告警规则处理
应用层-event_log记录
记录告警规则调整的决策和执行过程
应用层-运行体检中心
指标分析层-指标下钻分析（AI）
定期调用AI对系统指标进行检测，实现定时系统安全体检
应用层-运行体检中心
应用层-event_log记录
记录定时体检系统指标的执行过程和结果
指标分析层
调用模块
被调用模块
说明
指标分析层-指标下钻分析
基础设施层-Prometheus&监控系统Adapter
获取指标数据用于下钻分析；获取系统告警信息，分析后决策是否调整告警规则
指标分析层-指标下钻分析
指标分析层-异常指标分析
对某一个异常指标进行下钻分析，定位问题根源
指标分析层-指标下钻分析
应用层-治愈行为处理
AI做出决策后调用治愈行为处理模块执行故障治愈
指标分析层-指标下钻分析
应用层-告警规则处理
AI做出决策后调用告警规则处理模块执行告警规则调整
指标分析层-指标下钻分析
应用层-event_log记录
记录AI每一步的数据获取、分析和决策过程
指标分析层-异常指标分析
基础设施层-Prometheus&监控系统Adapter
获取指标数据进行下钻分析
指标分析层-异常指标分析
基础设施层-日志查询
获取日志数据定位问题根源
指标分析层-异常指标分析
应用层-event_log记录
记录AI每一步数据获取、分析和决策过程
技术选型
- DB -> Postgres
- 后端web框架：fox(gin的包装）
- 日志记录库：zerolog
- 前端页面选型：Vue
- 前端Controller：fox

模块设计

告警规则及meta信息管理
告警规则添加流程

flowchart LR
    A[zeroops启动] --> B[读取告警规则的配置文件]
    B --> C{对比 alert_rules 表<br/>告警规则是否缺失}
    C -- 缺失 --> D[告警规则写入告警系统]
    D --> E((结束))
    C -- 缺失 --> F[alert_rules 表插入规则<br/>alert_rule_metas 插入默认配置]
    F --> G[(alert_rules<br/>alert_rule_metas)]
    classDef db fill:#e0f5e9,stroke:#000,stroke-width:2px;
    class G db;

⸻

告警规则 meta 变更流程

flowchart LR
    A((告警规则<br/>变更调用)) --> B[告警规则管理]
    B --> C[修改指定规则的 meta 信息]
    C --> D[(alert_rule_metas)]
    B --> E[将修改 meta 的告警 rules<br/>更新进告警系统]
    E --> F[将 meta 数据更新为 metrics 接口数据<br/>使外部监控平台能够更新<br/>meta 对应的 metrics 数据]
    F --> G((结束))
    C --> H[告警变更记录]
    classDef db fill:#e0f5e9,stroke:#000,stroke-width:2px;
    class D db;

⸻
alertRules init 配置
这是MVP版本前期指定好的一些规则。
后期会允许用户通过告警平台页面管理告警规则

- 同一告警规则，多组告警阈值，如某个指标阈值90%是P0级，50%是P1级
  直接使用两条规则来进行实现
- 提供告警变更接口，参数：service+不同meta参数值更新，更新service_alert_metas表，并记录变更记录。
- 提供变更记录查询接口。

告警问题处理完整流程

flowchart LR
    A[收到告警] --> B[告警去重]
    B --> C[创建 issue]
    C --> D[异常等级计算]
    D --> E{是否严重<br/>只看异常等级}
    E -- 不严重 --> F[进入分析问题阶段]
    E -- 严重 --> G[确认告警对应的故障域]
    G --> H[故障域对应的解决问题的方式<br/>只支持回滚]
    H --> I[解决问题<br/>执行治愈操作]
    I --> F
    F --> J[指标下钻分析 AI]
    J --> K[多次调用<br/>分析关键指标]
    K --> L[异常指标分析]
    L --> M[AI 分析 comment 记录]
    J --> N[分析结果]
    N --> O{是否需要<br/>额外治愈动作}
    O -- 是 --> P[理解粒度的治愈动作]
    N --> Q{是否需要<br/>调整告警规则}
    Q -- 是 --> R[调整告警指标]
    J --> S{是否恢复<br/>issue 是否关闭}
    S -- 未恢复，继续下钻分析 --> J
    S -- 观察一段时间是否恢复 --> T[收到告警恢复]
    T --> U[close issue]

⸻
补充说明：
- 告警等级动态计算
  影响面重新收集、告警等级动态调整
- 告警去重功能（同一告警、labels相同时，在第一条未完成处理时，只触发一次）
  同一告警，新的更高等级，更新issue的等级列表 => 是否触发治愈动作？
- 不同等级的治愈行为处理
  P0需要有治愈动作

模块相关的数据表
- alert_rules：告警规则表。见上面alert_rules表结构
- alert_rule_metas：告警规则meta信息表。见上面alert_rule_metas表结构
- heal_actions：告警治愈的解决方案表。见上面resolve_actions表结构
- alert_meta_change_logs：告警规则变更记录
- alert_issues：记录告警事件issue

体检中心触发阶段

flowchart LR
    A[体检中心定时触发] --> B[收集所有指标列表<br/>依次对每个指标进行异常判断]
    B --> C[从 alert_rules 拉取所有 expr<br/>进行检查<br/>一条 expr 可能返回同一维度的多组数据<br/>如不同 service + version 各组数据<br/>分别进行检查]
    C --> D[单组指标数据<br/>是否有异常]
    D --> E[异常指标分析]
    E --> F{是否有异常}
    F -- 是 --> G{是否有告警触发}
    G -- 否 --> H[调整告警指标]


类图设计
⸻


运行体检中心模块会定期触发，每隔一段时间就检测系统的健康状态。首先是遍历所有服务列表，然后依次对每个服务的指标进行异常检测。如果判断出这个指标数据出现了异常，但是告警系统没有触发告警，就会相应去调整告警指标，具体包括调整告警阈值和持续时间。


设计目标
- 周期性：定时对全量服务指标进行异常检测。
- 智能化：利用时序异常检测算法识别阈值告警无法发现的异常模式。
- 闭环：对比异常检测结果与告警系统状态，生成或建议调整告警规则参数。
- 解耦：主流程使用Go语言编写，异常检测部分使用Python编写，将异常检测作为一个微服务板块，实现算法模块与主流程的解耦，便于独立迭代和部署

异常检测微服务 + 体检中心 + 外部依赖系统架构图

flowchart LR
    subgraph S1[异常检测微服务 Python]
        A1[算法模型：输出正常、异常二分类]
        A2[针对异常情况，AI<br/>具体分析异常区间<br/>和严重程度]
    end
    subgraph S2[运行体检中心 Go]
        B1[调度器]
        B2[指标采集器]
        B3[异常指标分析]
        B4{是否异常}
        B5[继续灰度发布]
        B6[调整告警规则]
        B1 -->|定时触发| B2
        B2 -->|获取指标数据| B3
        B3 --> B4
        B4 -- 正常 --> B5
        B4 -- 异常，且没有触发告警 --> B6
    end
    subgraph S3[外部依赖系统]
        C1[调用指标数据 API]
        C2[告警系统 API]
    end
    S2 -->|调用检测 API| S1
    S3 -->|调用| S2
    S2 -->|查询告警状态| S3


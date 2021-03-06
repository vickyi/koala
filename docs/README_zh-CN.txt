地方搜索请求

地方搜索请求是采用以下形式的 HTTP 网址：

https://maps.googleapis.com/maps/api/place/search/output?parameters
其中，output 可以是以下两个值中的任意一个：

json（建议），用于表示以 JavaScript 对象表示法 (JSON) 的形式输出
xml，用于表示以 XML 的形式输出
您需要使用某些参数，才能发起搜索请求。根据网址的标准，所有参数均使用和号字符 (&) 进行分隔。

必填参数

key，即您应用的 API 密钥。此密钥用于标识您的应用，以便管理配额，从而让您的应用可立即使用其中添加的地方信息。要创建 API 项目并获取密钥，请访问 API 控制台。
location，即要在其周围检索地方信息的纬度/经度。必须指定为纬度、经度。
radius，用于定义要在其范围内返回的地方结果的距离（以米为单位）。最大允许半径为 50,000 米。请注意，如果指定了 rankby=distance，则不得包含 radius（参见下文可选参数中的说明）。
sensor，用于表示发起相关地方请求的设备是否会使用 GPS 等位置传感器来确定该请求中发送的位置。该值必须是 true 或 false。
可选参数

keyword，即要与 Google 为该地方建立索引的全部内容相匹配的字词，包括但不限于名称、类型、地址以及客户的评论和任何第三方的内容。
language，即用于表示返回结果时应使用的语言（如果可能的话）的语言代码。请参阅支持的语言列表及其代码。请注意，我们会经常更新支持的语言，因此该列表可能并不详尽。
name，即要与地方信息的名称进行匹配的字词。这会将结果限制为包含传递的 name 值。
rankby，即用于指定结果的列出顺序。可能的值包括：
prominence（默认）：该选项根据其重要性对结果进行排序。排名将优先搜索指定区域内的著名地方。Google 索引中的地方排名、您应用中的报告位置次数、全球知名度和其他因素可能会对重要程度产生影响。
distance。该选项根据与指定的 location 之间的距离按升序方式对结果进行排序。按距离的结果排名将设置 50 千米的固定搜索半径。需要 keyword、name 或 types 中的一个或多个。
types，用于将结果限制为至少与一种指定类型相匹配的地方信息。类型应使用竖线符号 (type1|type2|etc) 进行分隔。请参阅支持的类型列表。
pagetoken，用于返回上一轮搜索的下一个 20 个结果。设置 pagetoken 参数后，系统将使用上一轮搜索的相同参数执行搜索，即除 pagetoken 外的所有参数将被忽略。
Maps API for Business 客户的搜索请求中不得包含 client 或 signature 参数。

以下是一个示例，其中展示了在以澳大利亚悉尼的一点为中心，半径为 500 米的范围内搜索名称包含“海港”一词且类型为“食品”的地方信息：

https://maps.googleapis.com/maps/api/place/search/json?location=-33.8670522,151.1957362&radius=500&types=food&name=harbour&sensor=false&key=AddYourOwnKeyHere
请注意，您需要将此示例中的密钥替换为自己的密钥，才能使该请求在您的应用中发挥作用。


JSON 响应最多包含四个根元素：

"status"，其中包含相关请求中的元数据。请参阅下面的状态代码。
"results"，其中包含一组分别带有各自相关信息的地方信息。有关这些结果的信息，请参阅地方搜索结果。Places API 针对每次查询返回多达 20 个 establishment 结果。此外，该 API 可能还会返回 political 结果，以用于标识请求的区域。
html_attributions，其中包含一组必须向用户显示的此商家信息的相关属性。
next_page_token，其中包含可用于返回多达 20 个其他结果的一个令牌。如果不存在可显示的其他结果，则不返回 next_page_token。返回的最大结果数为 60。从 next_page_token 发出到其生效，期间存在一个短暂的延迟。
要获取关于解析 JSON 响应的帮助，请参阅使用 JavaScript 处理 JSON。

状态代码

地方搜索响应对象中的 "status" 字段包含请求的状态，并且可能会包含调试信息，以帮助您找到地方搜索请求失败的原因。"status" 字段可能包含以下值：

OK，用于表示未发生错误；已成功检测到相应地方且至少返回了一个结果。
ZERO_RESULTS，用于表示搜索成功，但未返回任何结果。如果搜索中传递了一个位于偏远位置的 latlng，就会出现这种情况。
OVER_QUERY_LIMIT，用于表示您超出了自己的配额。
REQUEST_DENIED，用于表示您的请求遭拒，通常是由于缺少 sensor 参数。
INVALID_REQUEST，通常用于表示缺少必填参数（location 或 radius）。
搜索结果

当地方信息服务返回搜索所获得的 JSON 结果时，会将这些结果放在 results 数组中。即使未返回任何结果（例如，如果 location 过于遥远），该服务仍然会返回一个空的 results 数组。XML 响应不包含或包含多个 <result> 元素。

results 数组的每个元素均包含指定区域（location 和 radius）中的一个结果，并按照它们的重要程度排序。您应用中的签到活动会对结果的排序产生影响：近期签到次数较多的地方可能会更突出地显示在您应用的结果中。结果可能还包含必须向用户显示的属性信息。

results 数组中的每个结果均可能包含如下字段：

events[]：数组或一个或多个 <event> 元素提供该地方实事相关信息。每个地方最多返回三个活动，按照其开始时间排序。要了解活动的详情，请阅读 Places API 中的活动。每个活动均包含：
event_id：该活动的唯一 ID。
summary：活动的文字说明。此属性包含一个字符串，其内容未经服务器处理。您的应用应可以防止已被利用的漏洞，并且必要时进行妥善处理。
url：指向活动详情的网址。如果未指定该活动的网址，则不会返回此属性。
icon，其中包含可在显示此结果时向用户显示的推荐图标的网址。
id，其中包含表示此地方的唯一稳定标识符。此标识符可能无法用于检索此地方的相关信息，但可保证在各个会话中均有效。它还可用于合并此地方的相关数据，并在各个单独的搜索中验证该地方的同一性。
geometry，其中包含结果的几何图形信息，通常包括地方的 location（地址解析）和用于标识其常规覆盖区域的 viewport（可选）。
name，其中包含返回结果中可人工读取的名称。对于 establishment 结果，这通常是指商家名称。
opening_hours 可能包含以下信息：
open_now，即一个布尔值，用于表示该地方当前是否开放。
rating，其中包含根据用户评论得出的地方评分（0.0 至 5.0 之间）。
reference，其中包含唯一令牌，可用于在地方详情请求中检索关于相应地方的其他信息。您可以存储此令牌，并在日后随时用其来刷新关于相应地方的缓存数据，不过系统无法保证会在不同的搜索中针对任何给定地方返回同一令牌。
types[]，其中包含描述指定结果的特征类型数组。有关详情，请参阅支持的类型列表。如果为结果分配了多个类型，则 XML 响应将包含多个 <type> 元素。
vicinity，其中包含附近位置的地图项名称。通常，此地图项为给定结果中的街道或邻近地区。vicinity 属性是地方搜索的唯一返回结果。
formatted_address，即一个字符串，其中包含此地方的可人工读取地址。通常该地址就相当于“邮政地址”。formatted_address 属性是文本搜索的唯一返回结果。
访问其他结果

默认情况下，每个地方搜索针对每次查询返回多达 20 个 establishment 结果。不过，每个搜索可能会返回 60 个结果，分成三页显示。如果您的搜索返回 20 多个结果，则搜索响应会包含一个附加值 - next_page_token。将 next_page_token 的值传递到新搜索的 pagetoken 参数，查看下一个结果组。如果 next_page_token 为 Null，或未返回，则之后也不存在返回结果。

例如，在下列查询中，我们搜索澳大利亚悉尼达令海港附近的餐馆，并按距离对搜索结果进行排序。您可以看到响应包含一个 next_page_token 属性。


反向地理编码（地址查询）

“地理编码”这一术语通常指将易于理解的地址转换成地图上的一个点的过程。与此相反，将地图上的位置转换成易于理解的地址这一过程则称为“反向地理编码”。

Geocoding API 支持直接使用 latlng 参数进行反向地理编码。例如，以下查询包含了布鲁克林某一位置的纬度/经度值：

http://maps.googleapis.com/maps/api/geocode/json?latlng=40.714224,-73.961452&sensor=true_or_false
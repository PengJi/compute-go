# kombu
kombu 实现对 AMQP 的封装，对 AMQP transport和 non-AMQP transports(Redis、Amazon SQS、ZoopKeeper等)的兼容。
通过amqp 收发消息的过程：
* 消息从来不直接发送给队列，甚至 Producers 都可能不知道队列的存在。 消息是发送给交换机，给交换机发送消息时，需要指定消息的 routing_key 属性！
* 交换机收到消息后，根据 交换机的类型，或直接发送给队列 (fanout)， 或匹配消息的 routing_key 和 队列与交换机之间的 banding_key ;
  而topic类型 交换机匹配时，具有一些额外的特性，可以根据一些特殊字符进行匹配。 如果匹配，则递交消息给队列！
* Consumers 从队列取得消息；

即：消息发布者 Publisher 将 Message 发送给 Exchange 并且说明 Routing Key。
Exchange 负责根据 Message 的 Routing Key 进行路由，将 Message 正确地 转发给相应的 Message Queue。
监听在 Message Queue 上的 Consumer 将会从 Queue 中 读取消息。
Routing Key 是 Exchange 转发信息的依据，因此每个消息都有一个 Routing Key 表明可以接受消息的目的地址，
而每个 Message Queue 都可以通过将自己想要接收的 Routing Key 告诉 Exchange 进行 binding，
这样 Exchange 就可以将消息正确地转发给相应的 Message Queue。

# references
[Examples](https://docs.celeryproject.org/projects/kombu/en/stable/userguide/examples.html)
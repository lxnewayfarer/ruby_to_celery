require "bunny"

connection = Bunny.new
connection.start

channel = connection.create_channel
queue = channel.queue("requests")

correlation_id = rand(10_000_000).to_s

payload = "hello world"

exchange = channel.default_exchange

exchange.publish(
  payload,
  routing_key: queue.name,
  correlation_id: correlation_id,
  reply_to: "responses"
)

response = nil

queue_resp = channel.queue("responses")
queue_resp.subscribe(block: true, manual_ack: true) do |_delivery_info, properties, body|
  if properties[:correlation_id] == correlation_id
    response = body
    channel.acknowledge(_delivery_info.delivery_tag, false)
    channel.ack(_delivery_info.delivery_tag)
  end
end


puts "Received response: #{response}"


connection.close

import sys

destination_vm_ip = sys.argv[1]

config = f"""<source>
    @type forward
    port 24224
</source>
<match **>
    @type kafka2
    brokers {destination_vm_ip}:9092
    topic_key topic
    default_topic logs
    <buffer>
        @type memory
        chunk_limit_size 512k
        chunk_limit_records 50
        flush_mode immediate
        flush_thread_count 4
        queued_chunks_limit_size 32
        timekey 1s
        timekey_wait 0.1s
    </buffer>
    <format>
        @type json
    </format>
</match>"""


with open("/etc/fluent/fluent.conf", mode="w+") as file:
    file.write(config)

FILE="./payload.so"
OUTPUT_DIR="./payload_chunks"
CHUNK_SIZE=2048

mkdir -p "$OUTPUT_DIR"
split -b $CHUNK_SIZE "$FILE" "$OUTPUT_DIR/"

OFFSET=0
for f in $OUTPUT_DIR/*; do  
    xxd -p -c 999999 "$f" > "$OUTPUT_DIR/hex_$OFFSET"
    rm "$f"
    OFFSET=$(($OFFSET + $CHUNK_SIZE))
done


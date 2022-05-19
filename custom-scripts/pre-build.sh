#!/bin/sh

make -C $BASE_DIR/../modules/simple_driver/
cp $BASE_DIR/../custom-scripts/S41network-config $BASE_DIR/target/etc/init.d
chmod +x $BASE_DIR/target/etc/init.d/S41network-config
echo "tracefs /sys/kernel/tracing tracefs 0 0" >> output/target/etc/fstab

#!/bin/bash

qemu_pid=$(pidof qemu-system-x86_64)
qemu_path="/proc/$qemu_pid"

# enter the task
cd "$qemu_path"/task || exit
# printout tid and name
tid_path=$(ls)
for tid in ${tid_path}
do
	echo -e "pid($tid) \c" "$tid" && cat "$tid"/comm
done

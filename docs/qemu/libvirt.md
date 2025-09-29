# [libvirt](https://gitlab.com/libvirt/libvirt)

# 安装
## 从源码安装
```bash
sudo apt -y install libgnutls-dane0 libgnutls-openssl27 libgnutls28-dev libgnutlsxx28 libnl-3-dev libnl-route-3-dev libpciaccess-dev libxml2-utils xsltproc libdevmapper-dev libyajl-dev libyajl2 libxml2-dev

git clone git@gitlab.com:libvirt/libvirt.git

cd $HOME
mkdir -p libvirt_build
cd libvirt

#  for libvirt 6.6.0 or older
mkdir build
cd build
../autogen.sh --prefix=/usr --enable-debug=yses
# 或
# --prefix=$HOME/libvirt_build \
make -j$(nproc)
# make install is required only once to generate the config and log file structure
sudo make install

#  for libvirt 6.7.0 or later
meson build --prefix=/usr --debug
# 或
# meson build --prefix=$HOME/libvirt_build --debug
ninja -C build
# ninja -C build install is required only once to generate the config and log file structure
sudo ninja -C build install

# 安装过程
ninja: Entering directory `build'
[0/1] Installing files.
Installing src/libvirt_probes.stp to /usr/share/systemtap/tapset
Installing src/access/org.libvirt.api.policy to /usr/share/polkit-1/actions
Installing src/qemu/libvirt_qemu_probes.stp to /usr/share/systemtap/tapset
Installing src/libvirt.so.0.8000.0 to /usr/lib/x86_64-linux-gnu
Installing symlink pointing to libvirt.so.0.8000.0 to /usr/lib/x86_64-linux-gnu/libvirt.so.0
Installing symlink pointing to libvirt.so.0 to /usr/lib/x86_64-linux-gnu/libvirt.so
Installing src/libvirt-qemu.so.0.8000.0 to /usr/lib/x86_64-linux-gnu
Installing symlink pointing to libvirt-qemu.so.0.8000.0 to /usr/lib/x86_64-linux-gnu/libvirt-qemu.so.0
Installing symlink pointing to libvirt-qemu.so.0 to /usr/lib/x86_64-linux-gnu/libvirt-qemu.so
Installing src/libvirt-lxc.so.0.8000.0 to /usr/lib/x86_64-linux-gnu
Installing symlink pointing to libvirt-lxc.so.0.8000.0 to /usr/lib/x86_64-linux-gnu/libvirt-lxc.so.0
Installing symlink pointing to libvirt-lxc.so.0 to /usr/lib/x86_64-linux-gnu/libvirt-lxc.so
Installing src/libvirt-admin.so.0.8000.0 to /usr/lib/x86_64-linux-gnu
Installing symlink pointing to libvirt-admin.so.0.8000.0 to /usr/lib/x86_64-linux-gnu/libvirt-admin.so.0
Installing symlink pointing to libvirt-admin.so.0 to /usr/lib/x86_64-linux-gnu/libvirt-admin.so
Installing src/libvirt_driver_interface.so to /usr/lib/x86_64-linux-gnu/libvirt/connection-driver
Installing src/lockd.so to /usr/lib/x86_64-linux-gnu/libvirt/lock-driver
Installing src/libvirt_driver_network.so to /usr/lib/x86_64-linux-gnu/libvirt/connection-driver
Installing src/libvirt_driver_nodedev.so to /usr/lib/x86_64-linux-gnu/libvirt/connection-driver
Installing src/libvirt_driver_nwfilter.so to /usr/lib/x86_64-linux-gnu/libvirt/connection-driver
Installing src/libvirt_driver_secret.so to /usr/lib/x86_64-linux-gnu/libvirt/connection-driver
Installing src/libvirt_driver_storage.so to /usr/lib/x86_64-linux-gnu/libvirt/connection-driver
Installing src/libvirt_storage_backend_fs.so to /usr/lib/x86_64-linux-gnu/libvirt/storage-backend
Installing src/libvirt_storage_backend_iscsi-direct.so to /usr/lib/x86_64-linux-gnu/libvirt/storage-backend
Installing src/libvirt_storage_backend_logical.so to /usr/lib/x86_64-linux-gnu/libvirt/storage-backend
Installing src/libvirt_storage_backend_mpath.so to /usr/lib/x86_64-linux-gnu/libvirt/storage-backend
Installing src/libvirt_storage_backend_scsi.so to /usr/lib/x86_64-linux-gnu/libvirt/storage-backend
Installing src/libvirt_storage_backend_vstorage.so to /usr/lib/x86_64-linux-gnu/libvirt/storage-backend
Installing src/libvirt_storage_backend_zfs.so to /usr/lib/x86_64-linux-gnu/libvirt/storage-backend
Installing src/libvirt_storage_file_fs.so to /usr/lib/x86_64-linux-gnu/libvirt/storage-file
Installing src/libvirt_driver_lxc.so to /usr/lib/x86_64-linux-gnu/libvirt/connection-driver
Installing src/libvirt_driver_ch.so to /usr/lib/x86_64-linux-gnu/libvirt/connection-driver
Installing src/libvirt_driver_qemu.so to /usr/lib/x86_64-linux-gnu/libvirt/connection-driver
Installing src/libvirt_driver_vbox.so to /usr/lib/x86_64-linux-gnu/libvirt/connection-driver
Installing src/libvirtd to /usr/sbin
Installing src/virtproxyd to /usr/sbin
Installing src/virtinterfaced to /usr/sbin
Installing src/virtlockd to /usr/sbin
Installing src/virtlogd to /usr/sbin
Installing src/virtnetworkd to /usr/sbin
Installing src/virtnodedevd to /usr/sbin
Installing src/virtnwfilterd to /usr/sbin
Installing src/virtsecretd to /usr/sbin
Installing src/virtstoraged to /usr/sbin
Installing src/virtlxcd to /usr/sbin
Installing src/virtchd to /usr/sbin
Installing src/virtqemud to /usr/sbin
Installing src/virtvboxd to /usr/sbin
Installing src/libvirt_iohelper to /usr/libexec
Installing src/virt-ssh-helper to /usr/bin
Installing src/libvirt_leaseshelper to /usr/libexec
Installing src/libvirt_lxc to /usr/libexec
Installing src/virt-qemu-run to /usr/bin
Installing src/test_libvirt_lockd.aug to /usr/share/augeas/lenses/tests
Installing src/test_virtlockd.aug to /usr/share/augeas/lenses/tests
Installing src/test_virtlogd.aug to /usr/share/augeas/lenses/tests
Installing src/test_libvirtd_lxc.aug to /usr/share/augeas/lenses/tests
Installing src/test_libvirtd_qemu.aug to /usr/share/augeas/lenses/tests
Installing src/test_libvirtd.aug to /usr/share/augeas/lenses/tests
Installing src/test_virtproxyd.aug to /usr/share/augeas/lenses/tests
Installing src/test_virtinterfaced.aug to /usr/share/augeas/lenses/tests
Installing src/test_virtnetworkd.aug to /usr/share/augeas/lenses/tests
Installing src/test_virtnodedevd.aug to /usr/share/augeas/lenses/tests
Installing src/test_virtnwfilterd.aug to /usr/share/augeas/lenses/tests
Installing src/test_virtsecretd.aug to /usr/share/augeas/lenses/tests
Installing src/test_virtstoraged.aug to /usr/share/augeas/lenses/tests
Installing src/test_virtlxcd.aug to /usr/share/augeas/lenses/tests
Installing src/test_virtchd.aug to /usr/share/augeas/lenses/tests
Installing src/test_virtqemud.aug to /usr/share/augeas/lenses/tests
Installing src/test_virtvboxd.aug to /usr/share/augeas/lenses/tests
Installing src/libvirt_functions.stp to /usr/share/systemtap/tapset
Installing tools/virt-host-validate to /usr/bin
Installing tools/virt-login-shell to /usr/bin
Installing tools/virt-login-shell-helper to /usr/libexec
Installing tools/virsh to /usr/bin
Installing tools/virt-admin to /usr/bin
Installing tools/virt-pki-query-dn to /usr/bin
Installing tools/nss/libnss_libvirt.so.2 to /usr/lib/x86_64-linux-gnu
Installing tools/nss/libnss_libvirt_guest.so.2 to /usr/lib/x86_64-linux-gnu
Installing po/as/LC_MESSAGES/libvirt.mo to /usr/share/locale/as/LC_MESSAGES
Installing po/bg/LC_MESSAGES/libvirt.mo to /usr/share/locale/bg/LC_MESSAGES
Installing po/bn_IN/LC_MESSAGES/libvirt.mo to /usr/share/locale/bn_IN/LC_MESSAGES
Installing po/bs/LC_MESSAGES/libvirt.mo to /usr/share/locale/bs/LC_MESSAGES
Installing po/ca/LC_MESSAGES/libvirt.mo to /usr/share/locale/ca/LC_MESSAGES
Installing po/cs/LC_MESSAGES/libvirt.mo to /usr/share/locale/cs/LC_MESSAGES
Installing po/da/LC_MESSAGES/libvirt.mo to /usr/share/locale/da/LC_MESSAGES
Installing po/de/LC_MESSAGES/libvirt.mo to /usr/share/locale/de/LC_MESSAGES
Installing po/el/LC_MESSAGES/libvirt.mo to /usr/share/locale/el/LC_MESSAGES
Installing po/en_GB/LC_MESSAGES/libvirt.mo to /usr/share/locale/en_GB/LC_MESSAGES
Installing po/es/LC_MESSAGES/libvirt.mo to /usr/share/locale/es/LC_MESSAGES
Installing po/fi/LC_MESSAGES/libvirt.mo to /usr/share/locale/fi/LC_MESSAGES
Installing po/fr/LC_MESSAGES/libvirt.mo to /usr/share/locale/fr/LC_MESSAGES
Installing po/gu/LC_MESSAGES/libvirt.mo to /usr/share/locale/gu/LC_MESSAGES
Installing po/hi/LC_MESSAGES/libvirt.mo to /usr/share/locale/hi/LC_MESSAGES
Installing po/hu/LC_MESSAGES/libvirt.mo to /usr/share/locale/hu/LC_MESSAGES
Installing po/id/LC_MESSAGES/libvirt.mo to /usr/share/locale/id/LC_MESSAGES
Installing po/it/LC_MESSAGES/libvirt.mo to /usr/share/locale/it/LC_MESSAGES
Installing po/ja/LC_MESSAGES/libvirt.mo to /usr/share/locale/ja/LC_MESSAGES
Installing po/kn/LC_MESSAGES/libvirt.mo to /usr/share/locale/kn/LC_MESSAGES
Installing po/ko/LC_MESSAGES/libvirt.mo to /usr/share/locale/ko/LC_MESSAGES
Installing po/mk/LC_MESSAGES/libvirt.mo to /usr/share/locale/mk/LC_MESSAGES
Installing po/ml/LC_MESSAGES/libvirt.mo to /usr/share/locale/ml/LC_MESSAGES
Installing po/mr/LC_MESSAGES/libvirt.mo to /usr/share/locale/mr/LC_MESSAGES
Installing po/ms/LC_MESSAGES/libvirt.mo to /usr/share/locale/ms/LC_MESSAGES
Installing po/nb/LC_MESSAGES/libvirt.mo to /usr/share/locale/nb/LC_MESSAGES
Installing po/nl/LC_MESSAGES/libvirt.mo to /usr/share/locale/nl/LC_MESSAGES
Installing po/or/LC_MESSAGES/libvirt.mo to /usr/share/locale/or/LC_MESSAGES
Installing po/pa/LC_MESSAGES/libvirt.mo to /usr/share/locale/pa/LC_MESSAGES
Installing po/pl/LC_MESSAGES/libvirt.mo to /usr/share/locale/pl/LC_MESSAGES
Installing po/pt_BR/LC_MESSAGES/libvirt.mo to /usr/share/locale/pt_BR/LC_MESSAGES
Installing po/pt/LC_MESSAGES/libvirt.mo to /usr/share/locale/pt/LC_MESSAGES
Installing po/ru/LC_MESSAGES/libvirt.mo to /usr/share/locale/ru/LC_MESSAGES
Installing po/sr@latin/LC_MESSAGES/libvirt.mo to /usr/share/locale/sr@latin/LC_MESSAGES
Installing po/sr/LC_MESSAGES/libvirt.mo to /usr/share/locale/sr/LC_MESSAGES
Installing po/sv/LC_MESSAGES/libvirt.mo to /usr/share/locale/sv/LC_MESSAGES
Installing po/ta/LC_MESSAGES/libvirt.mo to /usr/share/locale/ta/LC_MESSAGES
Installing po/te/LC_MESSAGES/libvirt.mo to /usr/share/locale/te/LC_MESSAGES
Installing po/uk/LC_MESSAGES/libvirt.mo to /usr/share/locale/uk/LC_MESSAGES
Installing po/vi/LC_MESSAGES/libvirt.mo to /usr/share/locale/vi/LC_MESSAGES
Installing po/zh_CN/LC_MESSAGES/libvirt.mo to /usr/share/locale/zh_CN/LC_MESSAGES
Installing po/zh_TW/LC_MESSAGES/libvirt.mo to /usr/share/locale/zh_TW/LC_MESSAGES
Installing po/tr/LC_MESSAGES/libvirt.mo to /usr/share/locale/tr/LC_MESSAGES
Installing po/si/LC_MESSAGES/libvirt.mo to /usr/share/locale/si/LC_MESSAGES
Installing docs/libvirt-api.xml to /usr/share/libvirt/api
Installing docs/libvirt-lxc-api.xml to /usr/share/libvirt/api
Installing docs/libvirt-qemu-api.xml to /usr/share/libvirt/api
Installing docs/libvirt-admin-api.xml to /usr/share/libvirt/api
Installing docs/404.html to /usr/share/doc/libvirt/html
Installing docs/bugs.html to /usr/share/doc/libvirt/html
Installing docs/cgroups.html to /usr/share/doc/libvirt/html
Installing docs/contact.html to /usr/share/doc/libvirt/html
Installing docs/contribute.html to /usr/share/doc/libvirt/html
Installing docs/csharp.html to /usr/share/doc/libvirt/html
Installing docs/dbus.html to /usr/share/doc/libvirt/html
Installing docs/devguide.html to /usr/share/doc/libvirt/html
Installing docs/docs.html to /usr/share/doc/libvirt/html
Installing docs/downloads.html to /usr/share/doc/libvirt/html
Installing docs/drivers.html to /usr/share/doc/libvirt/html
Installing docs/drvbhyve.html to /usr/share/doc/libvirt/html
Installing docs/drvesx.html to /usr/share/doc/libvirt/html
Installing docs/drvhyperv.html to /usr/share/doc/libvirt/html
Installing docs/drvlxc.html to /usr/share/doc/libvirt/html
Installing docs/drvnodedev.html to /usr/share/doc/libvirt/html
Installing docs/drvopenvz.html to /usr/share/doc/libvirt/html
Installing docs/drvremote.html to /usr/share/doc/libvirt/html
Installing docs/drvsecret.html to /usr/share/doc/libvirt/html
Installing docs/drvtest.html to /usr/share/doc/libvirt/html
Installing docs/drvvbox.html to /usr/share/doc/libvirt/html
Installing docs/drvvirtuozzo.html to /usr/share/doc/libvirt/html
Installing docs/drvvmware.html to /usr/share/doc/libvirt/html
Installing docs/drvxen.html to /usr/share/doc/libvirt/html
Installing docs/errors.html to /usr/share/doc/libvirt/html
Installing docs/firewall.html to /usr/share/doc/libvirt/html
Installing docs/formatcaps.html to /usr/share/doc/libvirt/html
Installing docs/formatdomaincaps.html to /usr/share/doc/libvirt/html
Installing docs/format.html to /usr/share/doc/libvirt/html
Installing docs/formatnetwork.html to /usr/share/doc/libvirt/html
Installing docs/formatnetworkport.html to /usr/share/doc/libvirt/html
Installing docs/formatnode.html to /usr/share/doc/libvirt/html
Installing docs/formatnwfilter.html to /usr/share/doc/libvirt/html
Installing docs/formatsecret.html to /usr/share/doc/libvirt/html
Installing docs/formatsnapshot.html to /usr/share/doc/libvirt/html
Installing docs/formatstoragecaps.html to /usr/share/doc/libvirt/html
Installing docs/formatstorageencryption.html to /usr/share/doc/libvirt/html
Installing docs/goals.html to /usr/share/doc/libvirt/html
Installing docs/governance.html to /usr/share/doc/libvirt/html
Installing docs/hooks.html to /usr/share/doc/libvirt/html
Installing docs/index.html to /usr/share/doc/libvirt/html
Installing docs/internals.html to /usr/share/doc/libvirt/html
Installing docs/java.html to /usr/share/doc/libvirt/html
Installing docs/logging.html to /usr/share/doc/libvirt/html
Installing docs/nss.html to /usr/share/doc/libvirt/html
Installing docs/pci-hotplug.html to /usr/share/doc/libvirt/html
Installing docs/php.html to /usr/share/doc/libvirt/html
Installing docs/python.html to /usr/share/doc/libvirt/html
Installing docs/remote.html to /usr/share/doc/libvirt/html
Installing docs/securityprocess.html to /usr/share/doc/libvirt/html
Installing docs/storage.html to /usr/share/doc/libvirt/html
Installing docs/strategy.html to /usr/share/doc/libvirt/html
Installing docs/support.html to /usr/share/doc/libvirt/html
Installing docs/testapi.html to /usr/share/doc/libvirt/html
Installing docs/testsuites.html to /usr/share/doc/libvirt/html
Installing docs/testtck.html to /usr/share/doc/libvirt/html
Installing docs/tlscerts.html to /usr/share/doc/libvirt/html
Installing docs/uri.html to /usr/share/doc/libvirt/html
Installing docs/virshcmdref.html to /usr/share/doc/libvirt/html
Installing docs/windows.html to /usr/share/doc/libvirt/html
Installing docs/aclpolkit.html to /usr/share/doc/libvirt/html
Installing docs/advanced-tests.html to /usr/share/doc/libvirt/html
Installing docs/api_extension.html to /usr/share/doc/libvirt/html
Installing docs/api.html to /usr/share/doc/libvirt/html
Installing docs/apps.html to /usr/share/doc/libvirt/html
Installing docs/auditlog.html to /usr/share/doc/libvirt/html
Installing docs/auth.html to /usr/share/doc/libvirt/html
Installing docs/bindings.html to /usr/share/doc/libvirt/html
Installing docs/best-practices.html to /usr/share/doc/libvirt/html
Installing docs/ci.html to /usr/share/doc/libvirt/html
Installing docs/coding-style.html to /usr/share/doc/libvirt/html
Installing docs/committer-guidelines.html to /usr/share/doc/libvirt/html
Installing docs/compiling.html to /usr/share/doc/libvirt/html
Installing docs/daemons.html to /usr/share/doc/libvirt/html
Installing docs/developer-tooling.html to /usr/share/doc/libvirt/html
Installing docs/drvqemu.html to /usr/share/doc/libvirt/html
Installing docs/drvch.html to /usr/share/doc/libvirt/html
Installing docs/formatbackup.html to /usr/share/doc/libvirt/html
Installing docs/formatcheckpoint.html to /usr/share/doc/libvirt/html
Installing docs/formatdomain.html to /usr/share/doc/libvirt/html
Installing docs/formatstorage.html to /usr/share/doc/libvirt/html
Installing docs/glib-adoption.html to /usr/share/doc/libvirt/html
Installing docs/hacking.html to /usr/share/doc/libvirt/html
Installing docs/libvirt-go.html to /usr/share/doc/libvirt/html
Installing docs/libvirt-go-xml.html to /usr/share/doc/libvirt/html
Installing docs/migration.html to /usr/share/doc/libvirt/html
Installing docs/newreposetup.html to /usr/share/doc/libvirt/html
Installing docs/pci-addresses.html to /usr/share/doc/libvirt/html
Installing docs/platforms.html to /usr/share/doc/libvirt/html
Installing docs/programming-languages.html to /usr/share/doc/libvirt/html
Installing docs/styleguide.html to /usr/share/doc/libvirt/html
Installing docs/submitting-patches.html to /usr/share/doc/libvirt/html
Installing docs/acl.html to /usr/share/doc/libvirt/html
Installing docs/hvsupport.html to /usr/share/doc/libvirt/html
Installing docs/news.html to /usr/share/doc/libvirt/html
Installing docs/go/libvirt.html to /usr/share/doc/libvirt/html/go
Installing docs/go/libvirtxml.html to /usr/share/doc/libvirt/html/go
Installing docs/html/index.html to /usr/share/doc/libvirt/html/html
Installing docs/html/libvirt-libvirt-common.html to /usr/share/doc/libvirt/html/html
Installing docs/html/libvirt-libvirt-domain.html to /usr/share/doc/libvirt/html/html
Installing docs/html/libvirt-libvirt-domain-checkpoint.html to /usr/share/doc/libvirt/html/html
Installing docs/html/libvirt-libvirt-domain-snapshot.html to /usr/share/doc/libvirt/html/html
Installing docs/html/libvirt-libvirt-event.html to /usr/share/doc/libvirt/html/html
Installing docs/html/libvirt-libvirt-host.html to /usr/share/doc/libvirt/html/html
Installing docs/html/libvirt-libvirt-interface.html to /usr/share/doc/libvirt/html/html
Installing docs/html/libvirt-libvirt-network.html to /usr/share/doc/libvirt/html/html
Installing docs/html/libvirt-libvirt-nodedev.html to /usr/share/doc/libvirt/html/html
Installing docs/html/libvirt-libvirt-nwfilter.html to /usr/share/doc/libvirt/html/html
Installing docs/html/libvirt-libvirt-secret.html to /usr/share/doc/libvirt/html/html
Installing docs/html/libvirt-libvirt-storage.html to /usr/share/doc/libvirt/html/html
Installing docs/html/libvirt-libvirt-stream.html to /usr/share/doc/libvirt/html/html
Installing docs/html/libvirt-virterror.html to /usr/share/doc/libvirt/html/html
Installing docs/html/index-admin.html to /usr/share/doc/libvirt/html/html
Installing docs/html/libvirt-libvirt-admin.html to /usr/share/doc/libvirt/html/html
Installing docs/html/index-lxc.html to /usr/share/doc/libvirt/html/html
Installing docs/html/libvirt-libvirt-lxc.html to /usr/share/doc/libvirt/html/html
Installing docs/html/index-qemu.html to /usr/share/doc/libvirt/html/html
Installing docs/html/libvirt-libvirt-qemu.html to /usr/share/doc/libvirt/html/html
Installing docs/internals/command.html to /usr/share/doc/libvirt/html/internals
Installing docs/internals/eventloop.html to /usr/share/doc/libvirt/html/internals
Installing docs/internals/locking.html to /usr/share/doc/libvirt/html/internals
Installing docs/internals/rpc.html to /usr/share/doc/libvirt/html/internals
Installing docs/kbase/backing_chains.html to /usr/share/doc/libvirt/html/kbase
Installing docs/kbase/debuglogs.html to /usr/share/doc/libvirt/html/kbase
Installing docs/kbase/domainstatecapture.html to /usr/share/doc/libvirt/html/kbase
Installing docs/kbase/incrementalbackupinternals.html to /usr/share/doc/libvirt/html/kbase
Installing docs/kbase/index.html to /usr/share/doc/libvirt/html/kbase
Installing docs/kbase/kvm-realtime.html to /usr/share/doc/libvirt/html/kbase
Installing docs/kbase/launch_security_sev.html to /usr/share/doc/libvirt/html/kbase
Installing docs/kbase/live_full_disk_backup.html to /usr/share/doc/libvirt/html/kbase
Installing docs/kbase/locking-lockd.html to /usr/share/doc/libvirt/html/kbase
Installing docs/kbase/locking.html to /usr/share/doc/libvirt/html/kbase
Installing docs/kbase/locking-sanlock.html to /usr/share/doc/libvirt/html/kbase
Installing docs/kbase/memorydevices.html to /usr/share/doc/libvirt/html/kbase
Installing docs/kbase/merging_disk_image_chains.html to /usr/share/doc/libvirt/html/kbase
Installing docs/kbase/migrationinternals.html to /usr/share/doc/libvirt/html/kbase
Installing docs/kbase/qemu-core-dump.html to /usr/share/doc/libvirt/html/kbase
Installing docs/kbase/qemu-passthrough-security.html to /usr/share/doc/libvirt/html/kbase
Installing docs/kbase/rpm-deployment.html to /usr/share/doc/libvirt/html/kbase
Installing docs/kbase/s390_protected_virt.html to /usr/share/doc/libvirt/html/kbase
Installing docs/kbase/secureusage.html to /usr/share/doc/libvirt/html/kbase
Installing docs/kbase/systemtap.html to /usr/share/doc/libvirt/html/kbase
Installing docs/kbase/virtiofs.html to /usr/share/doc/libvirt/html/kbase
Installing docs/manpages/virsh.1 to /usr/share/man/man1
Installing docs/manpages/virt-admin.1 to /usr/share/man/man1
Installing docs/manpages/virt-host-validate.1 to /usr/share/man/man1
Installing docs/manpages/virt-login-shell.1 to /usr/share/man/man1
Installing docs/manpages/virt-pki-query-dn.1 to /usr/share/man/man1
Installing docs/manpages/virt-pki-validate.1 to /usr/share/man/man1
Installing docs/manpages/virt-qemu-run.1 to /usr/share/man/man1
Installing docs/manpages/virt-xml-validate.1 to /usr/share/man/man1
Installing docs/manpages/libvirtd.8 to /usr/share/man/man8
Installing docs/manpages/virt-ssh-helper.8 to /usr/share/man/man8
Installing docs/manpages/virtinterfaced.8 to /usr/share/man/man8
Installing docs/manpages/virtlockd.8 to /usr/share/man/man8
Installing docs/manpages/virtlogd.8 to /usr/share/man/man8
Installing docs/manpages/virtlxcd.8 to /usr/share/man/man8
Installing docs/manpages/virtnetworkd.8 to /usr/share/man/man8
Installing docs/manpages/virtnodedevd.8 to /usr/share/man/man8
Installing docs/manpages/virtnwfilterd.8 to /usr/share/man/man8
Installing docs/manpages/virtproxyd.8 to /usr/share/man/man8
Installing docs/manpages/virtqemud.8 to /usr/share/man/man8
Installing docs/manpages/virtsecretd.8 to /usr/share/man/man8
Installing docs/manpages/virtstoraged.8 to /usr/share/man/man8
Installing docs/manpages/virtvboxd.8 to /usr/share/man/man8
Installing docs/manpages/virkeycode-atset1.7 to /usr/share/man/man7
Installing docs/manpages/virkeycode-atset2.7 to /usr/share/man/man7
Installing docs/manpages/virkeycode-atset3.7 to /usr/share/man/man7
Installing docs/manpages/virkeycode-linux.7 to /usr/share/man/man7
Installing docs/manpages/virkeycode-osx.7 to /usr/share/man/man7
Installing docs/manpages/virkeycode-qnum.7 to /usr/share/man/man7
Installing docs/manpages/virkeycode-usb.7 to /usr/share/man/man7
Installing docs/manpages/virkeycode-win32.7 to /usr/share/man/man7
Installing docs/manpages/virkeycode-xtkbd.7 to /usr/share/man/man7
Installing docs/manpages/virkeyname-linux.7 to /usr/share/man/man7
Installing docs/manpages/virkeyname-osx.7 to /usr/share/man/man7
Installing docs/manpages/virkeyname-win32.7 to /usr/share/man/man7
Installing docs/manpages/index.html to /usr/share/doc/libvirt/html/manpages
Installing docs/manpages/virsh.html to /usr/share/doc/libvirt/html/manpages
Installing docs/manpages/virt-admin.html to /usr/share/doc/libvirt/html/manpages
Installing docs/manpages/virt-host-validate.html to /usr/share/doc/libvirt/html/manpages
Installing docs/manpages/virt-login-shell.html to /usr/share/doc/libvirt/html/manpages
Installing docs/manpages/virt-pki-query-dn.html to /usr/share/doc/libvirt/html/manpages
Installing docs/manpages/virt-pki-validate.html to /usr/share/doc/libvirt/html/manpages
Installing docs/manpages/virt-qemu-run.html to /usr/share/doc/libvirt/html/manpages
Installing docs/manpages/virt-xml-validate.html to /usr/share/doc/libvirt/html/manpages
Installing docs/manpages/libvirtd.html to /usr/share/doc/libvirt/html/manpages
Installing docs/manpages/virt-sanlock-cleanup.html to /usr/share/doc/libvirt/html/manpages
Installing docs/manpages/virt-ssh-helper.html to /usr/share/doc/libvirt/html/manpages
Installing docs/manpages/virtbhyved.html to /usr/share/doc/libvirt/html/manpages
Installing docs/manpages/virtinterfaced.html to /usr/share/doc/libvirt/html/manpages
Installing docs/manpages/virtlockd.html to /usr/share/doc/libvirt/html/manpages
Installing docs/manpages/virtlogd.html to /usr/share/doc/libvirt/html/manpages
Installing docs/manpages/virtlxcd.html to /usr/share/doc/libvirt/html/manpages
Installing docs/manpages/virtnetworkd.html to /usr/share/doc/libvirt/html/manpages
Installing docs/manpages/virtnodedevd.html to /usr/share/doc/libvirt/html/manpages
Installing docs/manpages/virtnwfilterd.html to /usr/share/doc/libvirt/html/manpages
Installing docs/manpages/virtproxyd.html to /usr/share/doc/libvirt/html/manpages
Installing docs/manpages/virtqemud.html to /usr/share/doc/libvirt/html/manpages
Installing docs/manpages/virtsecretd.html to /usr/share/doc/libvirt/html/manpages
Installing docs/manpages/virtstoraged.html to /usr/share/doc/libvirt/html/manpages
Installing docs/manpages/virtvboxd.html to /usr/share/doc/libvirt/html/manpages
Installing docs/manpages/virtvzd.html to /usr/share/doc/libvirt/html/manpages
Installing docs/manpages/virtxend.html to /usr/share/doc/libvirt/html/manpages
Installing docs/manpages/virkeycode-atset1.html to /usr/share/doc/libvirt/html/manpages
Installing docs/manpages/virkeycode-atset2.html to /usr/share/doc/libvirt/html/manpages
Installing docs/manpages/virkeycode-atset3.html to /usr/share/doc/libvirt/html/manpages
Installing docs/manpages/virkeycode-linux.html to /usr/share/doc/libvirt/html/manpages
Installing docs/manpages/virkeycode-osx.html to /usr/share/doc/libvirt/html/manpages
Installing docs/manpages/virkeycode-qnum.html to /usr/share/doc/libvirt/html/manpages
Installing docs/manpages/virkeycode-usb.html to /usr/share/doc/libvirt/html/manpages
Installing docs/manpages/virkeycode-win32.html to /usr/share/doc/libvirt/html/manpages
Installing docs/manpages/virkeycode-xtkbd.html to /usr/share/doc/libvirt/html/manpages
Installing docs/manpages/virkeyname-linux.html to /usr/share/doc/libvirt/html/manpages
Installing docs/manpages/virkeyname-osx.html to /usr/share/doc/libvirt/html/manpages
Installing docs/manpages/virkeyname-win32.html to /usr/share/doc/libvirt/html/manpages
Installing /home/jipeng/libvirt/include/libvirt/libvirt-admin.h to /usr/include/libvirt
Installing /home/jipeng/libvirt/include/libvirt/libvirt-domain-checkpoint.h to /usr/include/libvirt
Installing /home/jipeng/libvirt/include/libvirt/libvirt-domain.h to /usr/include/libvirt
Installing /home/jipeng/libvirt/include/libvirt/libvirt-domain-snapshot.h to /usr/include/libvirt
Installing /home/jipeng/libvirt/include/libvirt/libvirt-event.h to /usr/include/libvirt
Installing /home/jipeng/libvirt/include/libvirt/libvirt.h to /usr/include/libvirt
Installing /home/jipeng/libvirt/include/libvirt/libvirt-host.h to /usr/include/libvirt
Installing /home/jipeng/libvirt/include/libvirt/libvirt-interface.h to /usr/include/libvirt
Installing /home/jipeng/libvirt/include/libvirt/libvirt-lxc.h to /usr/include/libvirt
Installing /home/jipeng/libvirt/include/libvirt/libvirt-network.h to /usr/include/libvirt
Installing /home/jipeng/libvirt/include/libvirt/libvirt-nodedev.h to /usr/include/libvirt
Installing /home/jipeng/libvirt/include/libvirt/libvirt-nwfilter.h to /usr/include/libvirt
Installing /home/jipeng/libvirt/include/libvirt/libvirt-qemu.h to /usr/include/libvirt
Installing /home/jipeng/libvirt/include/libvirt/libvirt-secret.h to /usr/include/libvirt
Installing /home/jipeng/libvirt/include/libvirt/libvirt-storage.h to /usr/include/libvirt
Installing /home/jipeng/libvirt/include/libvirt/libvirt-stream.h to /usr/include/libvirt
Installing /home/jipeng/libvirt/include/libvirt/virterror.h to /usr/include/libvirt
Installing /home/jipeng/libvirt/build/include/libvirt/libvirt-common.h to /usr/include/libvirt
Installing /home/jipeng/libvirt/src/cpu_map/arm_cortex-a53.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/arm_cortex-a57.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/arm_cortex-a72.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/arm_Falkor.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/arm_FT-2000plus.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/arm_features.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/arm_Kunpeng-920.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/arm_Tengyun-S2500.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/arm_ThunderX299xx.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/arm_vendors.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/index.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/ppc64_POWER6.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/ppc64_POWER7.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/ppc64_POWER8.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/ppc64_POWER9.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/ppc64_POWERPC_e5500.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/ppc64_POWERPC_e6500.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/ppc64_vendors.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_486.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_athlon.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_Broadwell-IBRS.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_Broadwell-noTSX-IBRS.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_Broadwell-noTSX.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_Broadwell.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_Cascadelake-Server-noTSX.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_Cascadelake-Server.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_Conroe.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_Cooperlake.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_core2duo.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_coreduo.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_cpu64-rhel5.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_cpu64-rhel6.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_Dhyana.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_EPYC-IBPB.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_EPYC.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_EPYC-Milan.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_EPYC-Rome.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_features.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_Haswell-IBRS.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_Haswell-noTSX-IBRS.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_Haswell-noTSX.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_Haswell.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_Icelake-Client-noTSX.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_Icelake-Client.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_Icelake-Server-noTSX.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_Icelake-Server.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_IvyBridge-IBRS.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_IvyBridge.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_kvm32.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_kvm64.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_n270.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_Nehalem-IBRS.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_Nehalem.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_Opteron_G1.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_Opteron_G2.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_Opteron_G3.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_Opteron_G4.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_Opteron_G5.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_Penryn.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_pentium.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_pentium2.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_pentium3.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_pentiumpro.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_phenom.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_qemu32.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_qemu64.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_SandyBridge-IBRS.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_SandyBridge.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_Skylake-Client-IBRS.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_Skylake-Client-noTSX-IBRS.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_Skylake-Client.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_Skylake-Server-IBRS.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_Skylake-Server-noTSX-IBRS.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_Skylake-Server.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_Snowridge.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_vendors.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_Westmere-IBRS.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/src/cpu_map/x86_Westmere.xml to /usr/share/libvirt/cpu_map
Installing /home/jipeng/libvirt/build/src/remote/libvirtd.qemu.logrotate to /etc/logrotate.d
Installing /home/jipeng/libvirt/build/src/remote/libvirtd.lxc.logrotate to /etc/logrotate.d
Installing /home/jipeng/libvirt/build/src/remote/libvirtd.libxl.logrotate to /etc/logrotate.d
Installing /home/jipeng/libvirt/build/src/remote/libvirtd.logrotate to /etc/logrotate.d
Installing /home/jipeng/libvirt/src/remote/libvirtd.sysctl to /usr/lib/sysctl.d
Installing /home/jipeng/libvirt/src/remote/libvirtd.policy to /usr/share/polkit-1/actions
Installing /home/jipeng/libvirt/src/remote/libvirtd.rules to /usr/share/polkit-1/rules.d
Installing /home/jipeng/libvirt/build/src/network/default.xml to /etc/libvirt/qemu/networks
Installing /home/jipeng/libvirt/src/network/libvirt.zone to /usr/lib/firewalld/zones
Installing /home/jipeng/libvirt/src/nwfilter/xml/allow-arp.xml to /etc/libvirt/nwfilter
Installing /home/jipeng/libvirt/src/nwfilter/xml/allow-dhcp-server.xml to /etc/libvirt/nwfilter
Installing /home/jipeng/libvirt/src/nwfilter/xml/allow-dhcp.xml to /etc/libvirt/nwfilter
Installing /home/jipeng/libvirt/src/nwfilter/xml/allow-dhcpv6-server.xml to /etc/libvirt/nwfilter
Installing /home/jipeng/libvirt/src/nwfilter/xml/allow-dhcpv6.xml to /etc/libvirt/nwfilter
Installing /home/jipeng/libvirt/src/nwfilter/xml/allow-incoming-ipv4.xml to /etc/libvirt/nwfilter
Installing /home/jipeng/libvirt/src/nwfilter/xml/allow-incoming-ipv6.xml to /etc/libvirt/nwfilter
Installing /home/jipeng/libvirt/src/nwfilter/xml/allow-ipv4.xml to /etc/libvirt/nwfilter
Installing /home/jipeng/libvirt/src/nwfilter/xml/allow-ipv6.xml to /etc/libvirt/nwfilter
Installing /home/jipeng/libvirt/src/nwfilter/xml/clean-traffic-gateway.xml to /etc/libvirt/nwfilter
Installing /home/jipeng/libvirt/src/nwfilter/xml/clean-traffic.xml to /etc/libvirt/nwfilter
Installing /home/jipeng/libvirt/src/nwfilter/xml/no-arp-ip-spoofing.xml to /etc/libvirt/nwfilter
Installing /home/jipeng/libvirt/src/nwfilter/xml/no-arp-mac-spoofing.xml to /etc/libvirt/nwfilter
Installing /home/jipeng/libvirt/src/nwfilter/xml/no-arp-spoofing.xml to /etc/libvirt/nwfilter
Installing /home/jipeng/libvirt/src/nwfilter/xml/no-ip-multicast.xml to /etc/libvirt/nwfilter
Installing /home/jipeng/libvirt/src/nwfilter/xml/no-ip-spoofing.xml to /etc/libvirt/nwfilter
Installing /home/jipeng/libvirt/src/nwfilter/xml/no-ipv6-multicast.xml to /etc/libvirt/nwfilter
Installing /home/jipeng/libvirt/src/nwfilter/xml/no-ipv6-spoofing.xml to /etc/libvirt/nwfilter
Installing /home/jipeng/libvirt/src/nwfilter/xml/no-mac-broadcast.xml to /etc/libvirt/nwfilter
Installing /home/jipeng/libvirt/src/nwfilter/xml/no-mac-spoofing.xml to /etc/libvirt/nwfilter
Installing /home/jipeng/libvirt/src/nwfilter/xml/no-other-l2-traffic.xml to /etc/libvirt/nwfilter
Installing /home/jipeng/libvirt/src/nwfilter/xml/no-other-rarp-traffic.xml to /etc/libvirt/nwfilter
Installing /home/jipeng/libvirt/src/nwfilter/xml/qemu-announce-self-rarp.xml to /etc/libvirt/nwfilter
Installing /home/jipeng/libvirt/src/nwfilter/xml/qemu-announce-self.xml to /etc/libvirt/nwfilter
Installing /home/jipeng/libvirt/src/qemu/postcopy-migration.sysctl to /usr/lib/sysctl.d
Installing /home/jipeng/libvirt/src/test/test-screenshot.png to /usr/share/libvirt
Installing /home/jipeng/libvirt/src/admin/libvirt-admin.conf to /etc/libvirt
Installing /home/jipeng/libvirt/build/src/locking/qemu-lockd.conf to /etc/libvirt
Installing /home/jipeng/libvirt/src/locking/virtlockd.conf to /etc/libvirt
Installing /home/jipeng/libvirt/src/logging/virtlogd.conf to /etc/libvirt
Installing /home/jipeng/libvirt/src/lxc/lxc.conf to /etc/libvirt
Installing /home/jipeng/libvirt/src/qemu/qemu.conf to /etc/libvirt
Installing /home/jipeng/libvirt/src/libvirt.conf to /etc/libvirt
Installing /home/jipeng/libvirt/src/locking/libvirt_lockd.aug to /usr/share/augeas/lenses
Installing /home/jipeng/libvirt/src/locking/virtlockd.aug to /usr/share/augeas/lenses
Installing /home/jipeng/libvirt/src/logging/virtlogd.aug to /usr/share/augeas/lenses
Installing /home/jipeng/libvirt/src/lxc/libvirtd_lxc.aug to /usr/share/augeas/lenses
Installing /home/jipeng/libvirt/src/qemu/libvirtd_qemu.aug to /usr/share/augeas/lenses
Installing /home/jipeng/libvirt/build/src/libvirtd.conf to /etc/libvirt
Installing /home/jipeng/libvirt/build/src/libvirtd.aug to /usr/share/augeas/lenses
Installing /home/jipeng/libvirt/build/src/virtproxyd.conf to /etc/libvirt
Installing /home/jipeng/libvirt/build/src/virtproxyd.aug to /usr/share/augeas/lenses
Installing /home/jipeng/libvirt/build/src/virtinterfaced.conf to /etc/libvirt
Installing /home/jipeng/libvirt/build/src/virtinterfaced.aug to /usr/share/augeas/lenses
Installing /home/jipeng/libvirt/build/src/virtnetworkd.conf to /etc/libvirt
Installing /home/jipeng/libvirt/build/src/virtnetworkd.aug to /usr/share/augeas/lenses
Installing /home/jipeng/libvirt/build/src/virtnodedevd.conf to /etc/libvirt
Installing /home/jipeng/libvirt/build/src/virtnodedevd.aug to /usr/share/augeas/lenses
Installing /home/jipeng/libvirt/build/src/virtnwfilterd.conf to /etc/libvirt
Installing /home/jipeng/libvirt/build/src/virtnwfilterd.aug to /usr/share/augeas/lenses
Installing /home/jipeng/libvirt/build/src/virtsecretd.conf to /etc/libvirt
Installing /home/jipeng/libvirt/build/src/virtsecretd.aug to /usr/share/augeas/lenses
Installing /home/jipeng/libvirt/build/src/virtstoraged.conf to /etc/libvirt
Installing /home/jipeng/libvirt/build/src/virtstoraged.aug to /usr/share/augeas/lenses
Installing /home/jipeng/libvirt/build/src/virtlxcd.conf to /etc/libvirt
Installing /home/jipeng/libvirt/build/src/virtlxcd.aug to /usr/share/augeas/lenses
Installing /home/jipeng/libvirt/build/src/virtchd.conf to /etc/libvirt
Installing /home/jipeng/libvirt/build/src/virtchd.aug to /usr/share/augeas/lenses
Installing /home/jipeng/libvirt/build/src/virtqemud.conf to /etc/libvirt
Installing /home/jipeng/libvirt/build/src/virtqemud.aug to /usr/share/augeas/lenses
Installing /home/jipeng/libvirt/build/src/virtvboxd.conf to /etc/libvirt
Installing /home/jipeng/libvirt/build/src/virtvboxd.aug to /usr/share/augeas/lenses
Installing /home/jipeng/libvirt/src/remote/virt-guest-shutdown.target to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/libvirtd.service to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/libvirtd.socket to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/libvirtd-ro.socket to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/libvirtd-admin.socket to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/libvirtd-tcp.socket to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/libvirtd-tls.socket to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/virtproxyd.service to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/virtproxyd.socket to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/virtproxyd-ro.socket to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/virtproxyd-admin.socket to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/virtproxyd-tcp.socket to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/virtproxyd-tls.socket to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/virtinterfaced.service to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/virtinterfaced.socket to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/virtinterfaced-ro.socket to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/virtinterfaced-admin.socket to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/virtlockd.service to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/virtlockd.socket to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/virtlockd-admin.socket to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/virtlogd.service to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/virtlogd.socket to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/virtlogd-admin.socket to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/virtnetworkd.service to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/virtnetworkd.socket to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/virtnetworkd-ro.socket to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/virtnetworkd-admin.socket to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/virtnodedevd.service to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/virtnodedevd.socket to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/virtnodedevd-ro.socket to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/virtnodedevd-admin.socket to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/virtnwfilterd.service to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/virtnwfilterd.socket to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/virtnwfilterd-ro.socket to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/virtnwfilterd-admin.socket to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/virtsecretd.service to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/virtsecretd.socket to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/virtsecretd-ro.socket to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/virtsecretd-admin.socket to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/virtstoraged.service to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/virtstoraged.socket to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/virtstoraged-ro.socket to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/virtstoraged-admin.socket to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/virtlxcd.service to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/virtlxcd.socket to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/virtlxcd-ro.socket to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/virtlxcd-admin.socket to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/virtchd.service to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/virtchd.socket to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/virtchd-ro.socket to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/virtchd-admin.socket to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/virtqemud.service to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/virtqemud.socket to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/virtqemud-ro.socket to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/virtqemud-admin.socket to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/virtvboxd.service to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/virtvboxd.socket to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/virtvboxd-ro.socket to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/src/virtvboxd-admin.socket to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/src/remote/libvirtd.sysconf to /etc/sysconfig
Installing /home/jipeng/libvirt/src/remote/virtproxyd.sysconf to /etc/sysconfig
Installing /home/jipeng/libvirt/src/interface/virtinterfaced.sysconf to /etc/sysconfig
Installing /home/jipeng/libvirt/src/locking/virtlockd.sysconf to /etc/sysconfig
Installing /home/jipeng/libvirt/src/logging/virtlogd.sysconf to /etc/sysconfig
Installing /home/jipeng/libvirt/src/network/virtnetworkd.sysconf to /etc/sysconfig
Installing /home/jipeng/libvirt/src/node_device/virtnodedevd.sysconf to /etc/sysconfig
Installing /home/jipeng/libvirt/src/nwfilter/virtnwfilterd.sysconf to /etc/sysconfig
Installing /home/jipeng/libvirt/src/secret/virtsecretd.sysconf to /etc/sysconfig
Installing /home/jipeng/libvirt/src/storage/virtstoraged.sysconf to /etc/sysconfig
Installing /home/jipeng/libvirt/src/lxc/virtlxcd.sysconf to /etc/sysconfig
Installing /home/jipeng/libvirt/src/ch/virtchd.sysconf to /etc/sysconfig
Installing /home/jipeng/libvirt/src/qemu/virtqemud.sysconf to /etc/sysconfig
Installing /home/jipeng/libvirt/src/vbox/virtvboxd.sysconf to /etc/sysconfig
Installing /home/jipeng/libvirt/tools/virt-login-shell.conf to /etc/libvirt
Installing /home/jipeng/libvirt/build/tools/virt-xml-validate to /usr/bin
Installing /home/jipeng/libvirt/build/tools/virt-pki-validate to /usr/bin
Installing /home/jipeng/libvirt/build/tools/libvirt-guests.sh to /usr/libexec
Installing /home/jipeng/libvirt/tools/libvirt-guests.sysconf to /etc/sysconfig
Installing /home/jipeng/libvirt/build/tools/libvirt-guests.service to /usr/lib/systemd/system
Installing /home/jipeng/libvirt/build/tools/bash-completion/virsh to /usr/share/bash-completion/completions
Installing /home/jipeng/libvirt/build/tools/bash-completion/virt-admin to /usr/share/bash-completion/completions
Installing /home/jipeng/libvirt/examples/c/admin/client_close.c to /usr/share/doc/libvirt/examples/c/admin
Installing /home/jipeng/libvirt/examples/c/admin/client_info.c to /usr/share/doc/libvirt/examples/c/admin
Installing /home/jipeng/libvirt/examples/c/admin/client_limits.c to /usr/share/doc/libvirt/examples/c/admin
Installing /home/jipeng/libvirt/examples/c/admin/list_clients.c to /usr/share/doc/libvirt/examples/c/admin
Installing /home/jipeng/libvirt/examples/c/admin/list_servers.c to /usr/share/doc/libvirt/examples/c/admin
Installing /home/jipeng/libvirt/examples/c/admin/logging.c to /usr/share/doc/libvirt/examples/c/admin
Installing /home/jipeng/libvirt/examples/c/admin/threadpool_params.c to /usr/share/doc/libvirt/examples/c/admin
Installing /home/jipeng/libvirt/examples/c/domain/dommigrate.c to /usr/share/doc/libvirt/examples/c/domain
Installing /home/jipeng/libvirt/examples/c/domain/domtop.c to /usr/share/doc/libvirt/examples/c/domain
Installing /home/jipeng/libvirt/examples/c/domain/info1.c to /usr/share/doc/libvirt/examples/c/domain
Installing /home/jipeng/libvirt/examples/c/domain/rename.c to /usr/share/doc/libvirt/examples/c/domain
Installing /home/jipeng/libvirt/examples/c/domain/suspend.c to /usr/share/doc/libvirt/examples/c/domain
Installing /home/jipeng/libvirt/examples/c/misc/event-test.c to /usr/share/doc/libvirt/examples/c/misc
Installing /home/jipeng/libvirt/examples/c/misc/hellolibvirt.c to /usr/share/doc/libvirt/examples/c/misc
Installing /home/jipeng/libvirt/examples/c/misc/openauth.c to /usr/share/doc/libvirt/examples/c/misc
Installing /home/jipeng/libvirt/examples/polkit/libvirt-acl.rules to /usr/share/doc/libvirt/examples/polkit
Installing /home/jipeng/libvirt/examples/sh/virt-lxc-convert to /usr/share/doc/libvirt/examples/sh
Installing /home/jipeng/libvirt/examples/systemtap/rpc-monitor.stp to /usr/share/doc/libvirt/examples/systemtap
Installing /home/jipeng/libvirt/examples/systemtap/qemu-monitor.stp to /usr/share/doc/libvirt/examples/systemtap
Installing /home/jipeng/libvirt/examples/systemtap/lock-debug.stp to /usr/share/doc/libvirt/examples/systemtap
Installing /home/jipeng/libvirt/examples/systemtap/events.stp to /usr/share/doc/libvirt/examples/systemtap
Installing /home/jipeng/libvirt/examples/xml/storage/pool-dir.xml to /usr/share/doc/libvirt/examples/xml/storage
Installing /home/jipeng/libvirt/examples/xml/storage/pool-fs.xml to /usr/share/doc/libvirt/examples/xml/storage
Installing /home/jipeng/libvirt/examples/xml/storage/pool-logical.xml to /usr/share/doc/libvirt/examples/xml/storage
Installing /home/jipeng/libvirt/examples/xml/storage/pool-netfs.xml to /usr/share/doc/libvirt/examples/xml/storage
Installing /home/jipeng/libvirt/examples/xml/storage/vol-cow.xml to /usr/share/doc/libvirt/examples/xml/storage
Installing /home/jipeng/libvirt/examples/xml/storage/vol-qcow.xml to /usr/share/doc/libvirt/examples/xml/storage
Installing /home/jipeng/libvirt/examples/xml/storage/vol-qcow2.xml to /usr/share/doc/libvirt/examples/xml/storage
Installing /home/jipeng/libvirt/examples/xml/storage/vol-raw.xml to /usr/share/doc/libvirt/examples/xml/storage
Installing /home/jipeng/libvirt/examples/xml/storage/vol-sparse.xml to /usr/share/doc/libvirt/examples/xml/storage
Installing /home/jipeng/libvirt/examples/xml/storage/vol-vmdk.xml to /usr/share/doc/libvirt/examples/xml/storage
Installing /home/jipeng/libvirt/examples/xml/test/testdev.xml to /usr/share/doc/libvirt/examples/xml/test
Installing /home/jipeng/libvirt/examples/xml/test/testnodeinline.xml to /usr/share/doc/libvirt/examples/xml/test
Installing /home/jipeng/libvirt/examples/xml/test/testdomfc4.xml to /usr/share/doc/libvirt/examples/xml/test
Installing /home/jipeng/libvirt/examples/xml/test/testdomfv0.xml to /usr/share/doc/libvirt/examples/xml/test
Installing /home/jipeng/libvirt/examples/xml/test/testnode.xml to /usr/share/doc/libvirt/examples/xml/test
Installing /home/jipeng/libvirt/examples/xml/test/testnetdef.xml to /usr/share/doc/libvirt/examples/xml/test
Installing /home/jipeng/libvirt/examples/xml/test/testvol.xml to /usr/share/doc/libvirt/examples/xml/test
Installing /home/jipeng/libvirt/examples/xml/test/testnetpriv.xml to /usr/share/doc/libvirt/examples/xml/test
Installing /home/jipeng/libvirt/examples/xml/test/testpool.xml to /usr/share/doc/libvirt/examples/xml/test
Installing /home/jipeng/libvirt/docs/android-chrome-192x192.png to /usr/share/doc/libvirt/html
Installing /home/jipeng/libvirt/docs/android-chrome-256x256.png to /usr/share/doc/libvirt/html
Installing /home/jipeng/libvirt/docs/apple-touch-icon.png to /usr/share/doc/libvirt/html
Installing /home/jipeng/libvirt/docs/browserconfig.xml to /usr/share/doc/libvirt/html
Installing /home/jipeng/libvirt/docs/favicon.ico to /usr/share/doc/libvirt/html
Installing /home/jipeng/libvirt/docs/favicon-16x16.png to /usr/share/doc/libvirt/html
Installing /home/jipeng/libvirt/docs/favicon-32x32.png to /usr/share/doc/libvirt/html
Installing /home/jipeng/libvirt/docs/manifest.json to /usr/share/doc/libvirt/html
Installing /home/jipeng/libvirt/docs/mstile-150x150.png to /usr/share/doc/libvirt/html
Installing /home/jipeng/libvirt/docs/css/fonts.css to /usr/share/doc/libvirt/html/css
Installing /home/jipeng/libvirt/docs/css/generic.css to /usr/share/doc/libvirt/html/css
Installing /home/jipeng/libvirt/docs/css/libvirt.css to /usr/share/doc/libvirt/html/css
Installing /home/jipeng/libvirt/docs/css/main.css to /usr/share/doc/libvirt/html/css
Installing /home/jipeng/libvirt/docs/css/mobile.css to /usr/share/doc/libvirt/html/css
Installing /home/jipeng/libvirt/docs/fonts/LICENSE.rst to /usr/share/doc/libvirt/html/fonts
Installing /home/jipeng/libvirt/docs/fonts/overpass-bold-italic.woff to /usr/share/doc/libvirt/html/fonts
Installing /home/jipeng/libvirt/docs/fonts/overpass-bold.woff to /usr/share/doc/libvirt/html/fonts
Installing /home/jipeng/libvirt/docs/fonts/overpass-italic.woff to /usr/share/doc/libvirt/html/fonts
Installing /home/jipeng/libvirt/docs/fonts/overpass-light-italic.woff to /usr/share/doc/libvirt/html/fonts
Installing /home/jipeng/libvirt/docs/fonts/overpass-light.woff to /usr/share/doc/libvirt/html/fonts
Installing /home/jipeng/libvirt/docs/fonts/overpass-mono-bold.woff to /usr/share/doc/libvirt/html/fonts
Installing /home/jipeng/libvirt/docs/fonts/overpass-mono-light.woff to /usr/share/doc/libvirt/html/fonts
Installing /home/jipeng/libvirt/docs/fonts/overpass-mono-regular.woff to /usr/share/doc/libvirt/html/fonts
Installing /home/jipeng/libvirt/docs/fonts/overpass-mono-semibold.woff to /usr/share/doc/libvirt/html/fonts
Installing /home/jipeng/libvirt/docs/fonts/overpass-regular.woff to /usr/share/doc/libvirt/html/fonts
Installing /home/jipeng/libvirt/docs/html/home.png to /usr/share/doc/libvirt/html/html
Installing /home/jipeng/libvirt/docs/html/left.png to /usr/share/doc/libvirt/html/html
Installing /home/jipeng/libvirt/docs/html/right.png to /usr/share/doc/libvirt/html/html
Installing /home/jipeng/libvirt/docs/html/up.png to /usr/share/doc/libvirt/html/html
Installing /home/jipeng/libvirt/docs/images/event_loop_simple.png to /usr/share/doc/libvirt/html/images
Installing /home/jipeng/libvirt/docs/images/event_loop_worker.png to /usr/share/doc/libvirt/html/images
Installing /home/jipeng/libvirt/docs/images/libvirt-daemon-arch.png to /usr/share/doc/libvirt/html/images
Installing /home/jipeng/libvirt/docs/images/libvirt-driver-arch.png to /usr/share/doc/libvirt/html/images
Installing /home/jipeng/libvirt/docs/images/libvirt-object-model.png to /usr/share/doc/libvirt/html/images
Installing /home/jipeng/libvirt/docs/images/libvirt-virConnect-example.png to /usr/share/doc/libvirt/html/images
Installing /home/jipeng/libvirt/docs/images/migration-managed-direct.png to /usr/share/doc/libvirt/html/images
Installing /home/jipeng/libvirt/docs/images/migration-managed-p2p.png to /usr/share/doc/libvirt/html/images
Installing /home/jipeng/libvirt/docs/images/migration-native.png to /usr/share/doc/libvirt/html/images
Installing /home/jipeng/libvirt/docs/images/migration-tunnel.png to /usr/share/doc/libvirt/html/images
Installing /home/jipeng/libvirt/docs/images/migration-unmanaged-direct.png to /usr/share/doc/libvirt/html/images
Installing /home/jipeng/libvirt/docs/images/node.gif to /usr/share/doc/libvirt/html/images
Installing /home/jipeng/libvirt/docs/js/main.js to /usr/share/doc/libvirt/html/js
Installing /home/jipeng/libvirt/docs/logos/logo-banner-dark-256.png to /usr/share/doc/libvirt/html/logos
Installing /home/jipeng/libvirt/docs/logos/logo-banner-dark-800.png to /usr/share/doc/libvirt/html/logos
Installing /home/jipeng/libvirt/docs/logos/logo-banner-dark.svg to /usr/share/doc/libvirt/html/logos
Installing /home/jipeng/libvirt/docs/logos/logo-banner-light-256.png to /usr/share/doc/libvirt/html/logos
Installing /home/jipeng/libvirt/docs/logos/logo-banner-light-800.png to /usr/share/doc/libvirt/html/logos
Installing /home/jipeng/libvirt/docs/logos/logo-banner-light.svg to /usr/share/doc/libvirt/html/logos
Installing /home/jipeng/libvirt/docs/logos/logo-base.svg to /usr/share/doc/libvirt/html/logos
Installing /home/jipeng/libvirt/docs/logos/logo-square-128.png to /usr/share/doc/libvirt/html/logos
Installing /home/jipeng/libvirt/docs/logos/logo-square-192.png to /usr/share/doc/libvirt/html/logos
Installing /home/jipeng/libvirt/docs/logos/logo-square-256.png to /usr/share/doc/libvirt/html/logos
Installing /home/jipeng/libvirt/docs/logos/logo-square-96.png to /usr/share/doc/libvirt/html/logos
Installing /home/jipeng/libvirt/docs/logos/logo-square-powered-128.png to /usr/share/doc/libvirt/html/logos
Installing /home/jipeng/libvirt/docs/logos/logo-square-powered-192.png to /usr/share/doc/libvirt/html/logos
Installing /home/jipeng/libvirt/docs/logos/logo-square-powered-256.png to /usr/share/doc/libvirt/html/logos
Installing /home/jipeng/libvirt/docs/logos/logo-square-powered-96.png to /usr/share/doc/libvirt/html/logos
Installing /home/jipeng/libvirt/docs/logos/logo-square-powered.svg to /usr/share/doc/libvirt/html/logos
Installing /home/jipeng/libvirt/docs/logos/logo-square.svg to /usr/share/doc/libvirt/html/logos
Installing /home/jipeng/libvirt/docs/logos/logo-sticker-hexagon.svg to /usr/share/doc/libvirt/html/logos
Installing /home/jipeng/libvirt/docs/logos/logo-sticker-square.svg to /usr/share/doc/libvirt/html/logos
Installing /home/jipeng/libvirt/docs/schemas/basictypes.rng to /usr/share/libvirt/schemas
Installing /home/jipeng/libvirt/docs/schemas/capability.rng to /usr/share/libvirt/schemas
Installing /home/jipeng/libvirt/docs/schemas/cpu.rng to /usr/share/libvirt/schemas
Installing /home/jipeng/libvirt/docs/schemas/cputypes.rng to /usr/share/libvirt/schemas
Installing /home/jipeng/libvirt/docs/schemas/domainbackup.rng to /usr/share/libvirt/schemas
Installing /home/jipeng/libvirt/docs/schemas/domaincaps.rng to /usr/share/libvirt/schemas
Installing /home/jipeng/libvirt/docs/schemas/domaincheckpoint.rng to /usr/share/libvirt/schemas
Installing /home/jipeng/libvirt/docs/schemas/domaincommon.rng to /usr/share/libvirt/schemas
Installing /home/jipeng/libvirt/docs/schemas/domain.rng to /usr/share/libvirt/schemas
Installing /home/jipeng/libvirt/docs/schemas/domainsnapshot.rng to /usr/share/libvirt/schemas
Installing /home/jipeng/libvirt/docs/schemas/interface.rng to /usr/share/libvirt/schemas
Installing /home/jipeng/libvirt/docs/schemas/networkcommon.rng to /usr/share/libvirt/schemas
Installing /home/jipeng/libvirt/docs/schemas/networkport.rng to /usr/share/libvirt/schemas
Installing /home/jipeng/libvirt/docs/schemas/network.rng to /usr/share/libvirt/schemas
Installing /home/jipeng/libvirt/docs/schemas/nodedev.rng to /usr/share/libvirt/schemas
Installing /home/jipeng/libvirt/docs/schemas/nwfilterbinding.rng to /usr/share/libvirt/schemas
Installing /home/jipeng/libvirt/docs/schemas/nwfilter_params.rng to /usr/share/libvirt/schemas
Installing /home/jipeng/libvirt/docs/schemas/nwfilter.rng to /usr/share/libvirt/schemas
Installing /home/jipeng/libvirt/docs/schemas/secret.rng to /usr/share/libvirt/schemas
Installing /home/jipeng/libvirt/docs/schemas/storagecommon.rng to /usr/share/libvirt/schemas
Installing /home/jipeng/libvirt/docs/schemas/storagepoolcaps.rng to /usr/share/libvirt/schemas
Installing /home/jipeng/libvirt/docs/schemas/storagepool.rng to /usr/share/libvirt/schemas
Installing /home/jipeng/libvirt/docs/schemas/storagevol.rng to /usr/share/libvirt/schemas
Installing /home/jipeng/libvirt/build/libvirt.pc to /usr/lib/x86_64-linux-gnu/pkgconfig
Installing /home/jipeng/libvirt/build/libvirt-qemu.pc to /usr/lib/x86_64-linux-gnu/pkgconfig
Installing /home/jipeng/libvirt/build/libvirt-lxc.pc to /usr/lib/x86_64-linux-gnu/pkgconfig
Installing /home/jipeng/libvirt/build/libvirt-admin.pc to /usr/lib/x86_64-linux-gnu/pkgconfig
Running custom install script '/home/jipeng/libvirt/scripts/meson-python.sh /home/jipeng/.pyenv/shims/python3 /home/jipeng/libvirt/scripts/meson-install-symlink.py /etc/libvirt/qemu/networks/autostart ../default.xml default.xml'
Running custom install script '/home/jipeng/libvirt/scripts/meson-python.sh /home/jipeng/.pyenv/shims/python3 /home/jipeng/libvirt/scripts/meson-install-dirs.py /var/log/libvirt /var/lib/libvirt/lockd /var/lib/libvirt/lockd/files /var/run/libvirt/lockd /var/lib/libvirt/network /var/lib/libvirt/dnsmasq /var/run/libvirt/network /var/lib/libvirt/lxc /var/run/libvirt/lxc /var/log/libvirt/lxc /var/lib/libvirt/ch /var/run/libvirt/ch /var/lib/libvirt/qemu /var/run/libvirt/qemu /var/cache/libvirt/qemu /var/log/libvirt/qemu /var/lib/libvirt/swtpm /var/run/libvirt/qemu/swtpm /var/log/swtpm/libvirt/qemu /var/cache/libvirt /var/lib/libvirt/images /var/lib/libvirt/filesystems /var/lib/libvirt/boot'
```

编译 v6.2.0
```bash
git cherry-pick -x a5566155554ce8a43b1912188ae0879cfe2a26ad
git cherry-pick -x e71e13488dc1aa65456e54a4b41bc925821b4263
```

## 从 deb 包安装
```bash
sudo apt install libvirt-daemon virt-manager -y
```

[build libvirt](https://developer.ibm.com/tutorials/compiling-libvirt-and-qemu/)

## 常见错误
[启动 qemu 权限错误](https://unix.stackexchange.com/questions/471345/changing-libvirt-emulator-permission-denied)


# 一些典型的 libvirt xml
```xml
<!-- usb cdrom -->
<?xml version="1.0" encoding="utf-8"?>
<disk type="file" device="cdrom">
  <driver name="qemu" type="raw"/>
  <target dev="sdzy" bus="usb"/>
  <source file="/usr/share/smartx/images/vmtools/706dca56-06cc-4554-b74f-a686c8f973fb"/>
  <readonly/>
  <boot order='999'/>
  <address type='usb' bus='0' port='3'/>
</disk>

<!-- scsi cdrom -->
<?xml version="1.0" encoding="utf-8"?>
<disk type="file" device="cdrom">
  <driver name="qemu" type="raw"/>
  <target dev="sdzy" bus="scsi"/>
  <source file="/usr/share/smartx/images/8079ce65-0f2a-4059-bff0-2ffd4e264440"/>
  <readonly/>
  <boot order='999'/>
  <address type='drive' controller='0' bus='0' target='0' unit='2'/>
</disk>

<!-- usb disk -->
<disk type='file' device='disk'>
  <driver name='qemu' type='raw'/>
  <source file='/usr/share/smartx/images/ae5d0ad2-ee8b-4be8-a5e9-dd55f8beee62'/>
  <target dev='sdzy' bus='usb'/>
  <readonly/>
  <boot order='4'/>
  <address type='usb' bus='0' port='3'/>
</disk>
```

# 热添加设备
```bash
virsh attach-device 01d3658c-b11c-4e87-8214-512377513b31 usb_cdrom.xml --current
```

# 通过 libvirt 执行 qmp
```bash
# 使用 qmp 热添加 cdrom
virsh qemu-monitor-command ca4152ab-b978-4594-be4f-b41bb2532146 --pretty '{ "execute": "__com.redhat_drive_add", "arguments": { "id": "usb_cdrom_fastio_drive_id", "file":"/usr/share/smartx/images/d3420652-67a2-4121-a489-7d415039395d","media":"cdrom"}}'
virsh qemu-monitor-command ca4152ab-b978-4594-be4f-b41bb2532146 --pretty '{ "execute": "device_add", "arguments": { "driver": "usb-storage", "drive": "usb_cdrom_fastio_drive_id","bus": "usb.0", "port": "1" }}'

# 使用 hmp 热添加 cdrom
virsh qemu-monitor-command ca4152ab-b978-4594-be4f-b41bb2532146 --pretty '{ "execute": "human-monitor-command", "arguments": { "command-line": "drive_add auto id=usb_cdrom_drive,if=none,file=/usr/share/smartx/images/d3420652-67a2-4121-a489-7d415039395d,media=cdrom" } }'
virsh qemu-monitor-command ca4152ab-b978-4594-be4f-b41bb2532146 --pretty '{ "execute": "human-monitor-command", "arguments": { "command-line": "device_add usb-storage,id=usb_cdrom_device,drive=usb_cdrom_drive,bus=usb.0,port=2" }}'

# 使用 qmp 热删除 cdrom
virsh qemu-monitor-command ca4152ab-b978-4594-be4f-b41bb2532146 --pretty '{ "execute": "human-monitor-command", "arguments": { "command-line": "drive_del usb_cdrom_drive" } }'
virsh qemu-monitor-command ca4152ab-b978-4594-be4f-b41bb2532146 --pretty '{ "execute": "human-monitor-command", "arguments": { "command-line": "device_del usb_cdrom_device" } }'
```

# 通过 libvirt 执行 qga
```bash
# 测试虚拟机里的 qemu-guest-agent 是否可用
virsh qemu-agent-command ca4152ab-b978-4594-be4f-b41bb2532146 --pretty '{ "execute": "guest-ping" }'

# 查看支持的 qemu-guest-agent 指令
virsh qemu-agent-command ca4152ab-b978-4594-be4f-b41bb2532146 --pretty '{ "execute": "guest-info" }'

# 获得网卡信息
virsh qemu-agent-command ca4152ab-b978-4594-be4f-b41bb2532146 --pretty '{ "execute": "guest-network-get-interfaces" }'

# 执行命令，这是异步的，第一步会返回一个pid，假设为797，在第二步需要带上这个pid
virsh qemu-agent-command ca4152ab-b978-4594-be4f-b41bb2532146 --pretty '{ "execute": "guest-exec", "arguments": { "path": "ip", "arg": [ "addr", "list" ], "capture-output": true } }'
virsh qemu-agent-command ca4152ab-b978-4594-be4f-b41bb2532146 --pretty '{ "execute": "guest-exec-status", "arguments": { "pid": 797 } }'
```

# 管理虚拟机
[管理虚拟机](https://docs.openeuler.org/zh/docs/20.03_LTS/docs/Virtualization/%E7%AE%A1%E7%90%86%E8%99%9A%E6%8B%9F%E6%9C%BA.html)

# 其他命令
dump
当虚拟机状态异常时，比如无响应，可 dump 其内存状态。
```bash
virsh dump --memory-only --live e5fb54af-98ec-46d7-a69b-5a8fb6b52996 name.dump
crash vmlinux name.dump

# 查看任务状态
virsh domjobinfo e5fb54af-98ec-46d7-a69b-5a8fb6b52996
```
[20.19. Creating a Dump File of a Guest Virtual Machine's Core Using virsh dump](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/virtualization_deployment_and_administration_guide/sect-domain_commands-creating_a_dump_file_of_a_domains_core)


# libvirt Python 接口
 ```python
import logging
import traceback

import libvirt
import libvirt_qemu

DEFAULT_CMD_TIMEOUT = 10


class LibvirtLocalConnection(object):
    def __init__(self):
        self._conn = None
        self._domain_cache = {}

    @property
    def conn(self):
        if self._conn is None:
            self._conn = libvirt.open("qemu:///system")
        return self._conn

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            logging.error("libvirtError (%s)%s: %s", exc_type, exc_val, "".join(traceback.format_tb(exc_tb)))
        if self._conn:
            self._conn.close()

    def execute_qemu_agent_command(self, dom_name, command_json, timeout=None):
        """Run qga command

        command reference: https://qemu-project.gitlab.io/qemu/interop/qemu-ga-ref.html
        https://github.com/libvirt/libvirt/blob/master/src/libvirt-qemu.c
        :param dom_name: vm_uuid
        :param command_json: built-in commands or scripts
        :param timeout: maximum command execution time
        :return: commands result
        """
        try:
            if timeout is None:
                timeout = DEFAULT_CMD_TIMEOUT
            if dom_name not in self._domain_cache:
                self._domain_cache[dom_name] = self.conn.lookupByName(dom_name)
            dom = self._domain_cache[dom_name]
            # The flags parameter of qemuAgentCommand is reserved for future use that must just pass 0 for now
            return libvirt_qemu.qemuAgentCommand(dom, command_json, timeout, 0)
        except libvirt.libvirtError as excp:
            raise Exception(excp.message)

    def execute_qemu_monitor_command(self, dom_name, command_josn):
        """Run QMP command

        command reference: https://qemu-project.gitlab.io/qemu/interop/qemu-qmp-ref.html
        :param dom_name: vm_uuid
        :param command_josn: qmp command
        :return: commands result
        """
        try:
            if dom_name not in self._domain_cache:
                self._domain_cache[dom_name] = self.conn.lookupByName(dom_name)
            domain = self._domain_cache[dom_name]
            return libvirt_qemu.qemuMonitorCommand(
                domain, command_josn, libvirt_qemu.VIR_DOMAIN_QEMU_MONITOR_COMMAND_DEFAULT
            )
        except libvirt.libvirtError as excp:
            raise Exception(excp.message)


if __name__ == "__main__":
    import json

    with LibvirtLocalConnection() as conn:
        vm_uuid = "ca4152ab-b978-4594-be4f-b41bb2532146"
        cdrom_iso = "/usr/share/smartx/images/d3420652-67a2-4121-a489-7d415039395d"

        agent_command_args = {"execute": "guest-info"}
        # print(conn.execute_qemu_agent_command(vm_uuid, json.dumps(agent_command_args)))

        # hotplug cdrom
        drive_args = {
            "execute": "__com.redhat_drive_add",
            "arguments": {"id": "usb_cdrom_drive", "file": cdrom_iso, "media": "cdrom"},
        }f
        add_device_args = {
            "execute": "device_add",
            "arguments": {
                "driver": "usb-storage",
                "id": "usb_cdrom_device",
                "drive": "usb_cdrom_drive",
                "bus": "usb.0",
            },
        }
        print(conn.execute_qemu_monitor_command(vm_uuid, json.dumps(drive_args)))
        print(conn.execute_qemu_monitor_command(vm_uuid, json.dumps(add_device_args)))

        # run hmp by qmp
        hmp_drive_args = {
            "execute": "human-monitor-command",
            "arguments": {
                "command-line": "drive_add auto id=usb_cdrom_drive,if=none,file={},media=cdrom".format(cdrom_iso)
            },
        }
        hmp_add_device_args = {
            "execute": "human-monitor-command",
            "arguments": {"command-line": "device_add usb-storage,id=usb_cdrom_device,drive=usb_cdrom_drive,bus=usb.0"},
        }
        # print(conn.execute_qemu_monitor_command(vm_uuid, json.dumps(hmp_drive_args)))
        # print(conn.execute_qemu_monitor_command(vm_uuid, json.dumps(hmp_add_device_args)))

        # hot detach cdrom
        del_device_args = {"execute": "device_del", "arguments": {"id": "usb_cdrom_device"}}
        # print(conn.execute_qemu_monitor_command(vm_uuid, json.dumps(del_device_args)))
 ```

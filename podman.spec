# If any of the following macros should be set otherwise,
# you can wrap any of them with the following conditions:
# - %%if 0%%{centos} == 7
# - %%if 0%%{?rhel} == 7
# - %%if 0%%{?fedora} == 23
# Or just test for particular distribution:
# - %%if 0%%{centos}
# - %%if 0%%{?rhel}
# - %%if 0%%{?fedora}
#
# Be aware, on centos, both %%rhel and %%centos are set. If you want to test
# rhel specific macros, you can use %%if 0%%{?rhel} && 0%%{?centos} == 0 condition.
# (Don't forget to replace double percentage symbol with single one in order to apply a condition)

# Generate devel rpm
%global with_devel 0
# Build project from bundled dependencies
%global with_bundled 1
# Build with debug info rpm
%global with_debug 1
# Run tests in check section
%global with_check 0
# Generate unit-test rpm
%global with_unit_test 0

%if 0%{?fedora} >= 28
%bcond_without varlink
%else
%bcond_with varlink
%endif

%if 0%{?with_debug}
%global _find_debuginfo_dwz_opts %{nil}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

# %if ! 0% {?gobuild:1}
%define gobuild(o:) go build -tags="$BUILDTAGS selinux seccomp" -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n')" -a -v -x %{?**};
#% endif

%global provider github
%global provider_tld com
%global project projectatomic
%global repo libpod
# https://github.com/projectatomic/libpod
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path %{provider_prefix}
%global git0 https://%{provider}.%{provider_tld}/%{project}/%{repo}
%global commit0 208b9a6b6b250295759d3ef7d379b7b498144f4a
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

Name: podman
Version: 0.6.5
Release: 3.git%{shortcommit0}%{?dist}
Summary: Manage Pods, Containers and Container Images
License: ASL 2.0
URL: %{git_podman}
Source0: %{git0}/archive/%{commit0}/%{repo}-%{shortcommit0}.tar.gz
# e.g. el6 has ppc64 arch without gcc-go, so EA tag is required
#ExclusiveArch:  %%{?go_arches:%%{go_arches}}%%{!?go_arches:%%{ix86} x86_64 aarch64 %%{arm}}
ExclusiveArch: aarch64 %{arm} ppc64le s390x x86_64
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires: %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}
BuildRequires: btrfs-progs-devel
BuildRequires: device-mapper-devel
BuildRequires: glib2-devel
BuildRequires: glibc-devel
BuildRequires: glibc-static
BuildRequires: git
BuildRequires: go-md2man
BuildRequires: gpgme-devel
BuildRequires: libassuan-devel
BuildRequires: libgpg-error-devel
BuildRequires: libseccomp-devel
BuildRequires: libselinux-devel
BuildRequires: pkgconfig
BuildRequires: make
Requires: runc
Requires: containers-common
Requires: conmon >= 2:1.10.0-3.gitb0f6d98
Requires: buildah
Requires: containernetworking-cni >= 0.6.0-3
Requires: iptables
Requires: atomic-registries
Requires: oci-systemd-hook

# vendored libraries
# awk '{print "Provides: bundled(golang("$1")) = "$2}' vendor.conf | sort
# [thanks to Carl George <carl@george.computer> for containerd.spec]
Provides: bundled(golang(github.com/asaskevich/govalidator)) = v6
Provides: bundled(golang(github.com/Azure/go-ansiterm)) = 19f72df4d05d31cbe1c56bfc8045c96babff6c7e
Provides: bundled(golang(github.com/beorn7/perks)) = 3ac7bf7a47d159a033b107610db8a1b6575507a4
Provides: bundled(golang(github.com/blang/semver)) = v3.5.0
Provides: bundled(golang(github.com/buger/goterm)) = 2f8dfbc7dbbff5dd1d391ed91482c24df243b2d3
Provides: bundled(golang(github.com/BurntSushi/toml)) = v0.2.0
Provides: bundled(golang(github.com/containerd/cgroups)) = 7a5fdd8330119dc70d850260db8f3594d89d6943
Provides: bundled(golang(github.com/containerd/continuity)) = master
Provides: bundled(golang(github.com/containernetworking/cni)) = v0.4.0
Provides: bundled(golang(github.com/containers/image)) = b129a8413fd1e8c53379acbbacfc7b667070ae50
Provides: bundled(golang(github.com/containers/storage)) = 1e5ce40cdb84ab66e26186435b1273e04b879fef
Provides: bundled(golang(github.com/coreos/go-systemd)) = v14
Provides: bundled(golang(github.com/cyphar/filepath-securejoin)) = v0.2.1
Provides: bundled(golang(github.com/davecgh/go-spew)) = v1.1.0
Provides: bundled(golang(github.com/dgrijalva/jwt-go)) = v3.0.0
Provides: bundled(golang(github.com/docker/distribution)) = 7a8efe719e55bbfaff7bc5718cdf0ed51ca821df
Provides: bundled(golang(github.com/docker/docker)) = ce452fb72ffcdb7605ce98bde9302238f47c63c5
Provides: bundled(golang(github.com/docker/docker-credential-helpers)) = d68f9aeca33f5fd3f08eeae5e9d175edf4e731d1
Provides: bundled(golang(github.com/docker/go-connections)) = 3ede32e2033de7505e6500d6c868c2b9ed9f169d
Provides: bundled(golang(github.com/docker/go-units)) = v0.3.2
Provides: bundled(golang(github.com/docker/libtrust)) = aabc10ec26b754e797f9028f4589c5b7bd90dc20
Provides: bundled(golang(github.com/docker/spdystream)) = ed496381df8283605c435b86d4fdd6f4f20b8c6e
Provides: bundled(golang(github.com/emicklei/go-restful)) = ff4f55a206334ef123e4f79bbf348980da81ca46
Provides: bundled(golang(github.com/emicklei/go-restful-swagger12)) = 1.0.1
Provides: bundled(golang(github.com/exponent-io/jsonpath)) = d6023ce2651d8eafb5c75bb0c7167536102ec9f5
Provides: bundled(golang(github.com/fatih/camelcase)) = f6a740d52f961c60348ebb109adde9f4635d7540
Provides: bundled(golang(github.com/ghodss/yaml)) = 04f313413ffd65ce25f2541bfd2b2ceec5c0908c
Provides: bundled(golang(github.com/godbus/dbus)) = a389bdde4dd695d414e47b755e95e72b7826432c
Provides: bundled(golang(github.com/gogo/protobuf)) = v0.3
Provides: bundled(golang(github.com/golang/glog)) = 23def4e6c14b4da8ac2ed8007337bc5eb5007998
Provides: bundled(golang(github.com/golang/groupcache)) = b710c8433bd175204919eb38776e944233235d03
Provides: bundled(golang(github.com/golang/protobuf)) = 748d386b5c1ea99658fd69fe9f03991ce86a90c1
Provides: bundled(golang(github.com/google/gofuzz)) = 44d81051d367757e1c7c6a5a86423ece9afcf63c
Provides: bundled(golang(github.com/go-openapi/analysis)) = b44dc874b601d9e4e2f6e19140e794ba24bead3b
Provides: bundled(golang(github.com/go-openapi/errors)) = d24ebc2075bad502fac3a8ae27aa6dd58e1952dc
Provides: bundled(golang(github.com/go-openapi/jsonpointer)) = 779f45308c19820f1a69e9a4cd965f496e0da10f
Provides: bundled(golang(github.com/go-openapi/jsonreference)) = 36d33bfe519efae5632669801b180bf1a245da3b
Provides: bundled(golang(github.com/go-openapi/loads)) = 18441dfa706d924a39a030ee2c3b1d8d81917b38
Provides: bundled(golang(github.com/go-openapi/spec)) = 6aced65f8501fe1217321abf0749d354824ba2ff
Provides: bundled(golang(github.com/go-openapi/strfmt)) = 93a31ef21ac23f317792fff78f9539219dd74619
Provides: bundled(golang(github.com/go-openapi/swag)) = 1d0bd113de87027671077d3c71eb3ac5d7dbba72
Provides: bundled(golang(github.com/gorilla/context)) = v1.1
Provides: bundled(golang(github.com/gorilla/mux)) = v1.3.0
Provides: bundled(golang(github.com/hashicorp/errwrap)) = 7554cd9344cec97297fa6649b055a8c98c2a1e55
Provides: bundled(golang(github.com/hashicorp/golang-lru)) = 0a025b7e63adc15a622f29b0b2c4c3848243bbf6
Provides: bundled(golang(github.com/hashicorp/go-multierror)) = 83588e72410abfbe4df460eeb6f30841ae47d4c4
Provides: bundled(golang(github.com/imdario/mergo)) = 0.2.2
Provides: bundled(golang(github.com/juju/ratelimit)) = 5b9ff866471762aa2ab2dced63c9fb6f53921342
Provides: bundled(golang(github.com/kr/pty)) = v1.0.0
Provides: bundled(golang(github.com/mailru/easyjson)) = 99e922cf9de1bc0ab38310c277cff32c2147e747
Provides: bundled(golang(github.com/mattn/go-runewidth)) = v0.0.1
Provides: bundled(golang(github.com/matttproud/golang_protobuf_extensions)) = fc2b8d3a73c4867e51861bbdd5ae3c1f0869dd6a
Provides: bundled(golang(github.com/Microsoft/go-winio)) = 78439966b38d69bf38227fbf57ac8a6fee70f69a
Provides: bundled(golang(github.com/Microsoft/hcsshim)) = 43f9725307998e09f2e3816c2c0c36dc98f0c982
Provides: bundled(golang(github.com/mistifyio/go-zfs)) = v2.1.1
Provides: bundled(golang(github.com/mitchellh/mapstructure)) = d0303fe809921458f417bcf828397a65db30a7e4
Provides: bundled(golang(github.com/mtrmac/gpgme)) = b2432428689ca58c2b8e8dea9449d3295cf96fc9
Provides: bundled(golang(github.com/opencontainers/go-digest)) = v1.0.0-rc0
Provides: bundled(golang(github.com/opencontainers/image-spec)) = v1.0.0
Provides: bundled(golang(github.com/opencontainers/runc)) = 6e15bc3f92fd4c58b3285e8f27eaeb6b22d62920
Provides: bundled(golang(github.com/opencontainers/runtime-spec)) = v1.0.0
Provides: bundled(golang(github.com/opencontainers/runtime-tools)) = 625e2322645b151a7cbb93a8b42920933e72167f
Provides: bundled(golang(github.com/opencontainers/selinux)) = b29023b86e4a69d1b46b7e7b4e2b6fda03f0b9cd
Provides: bundled(golang(github.com/ostreedev/ostree-go)) = master
Provides: bundled(golang(github.com/pkg/errors)) = v0.8.0
Provides: bundled(golang(github.com/pmezard/go-difflib)) = 792786c7400a136282c1664665ae0a8db921c6c2
Provides: bundled(golang(github.com/pquerna/ffjson)) = d49c2bc1aa135aad0c6f4fc2056623ec78f5d5ac
Provides: bundled(golang(github.com/prometheus/client_golang)) = e7e903064f5e9eb5da98208bae10b475d4db0f8c
Provides: bundled(golang(github.com/prometheus/client_model)) = fa8ad6fec33561be4280a8f0514318c79d7f6cb6
Provides: bundled(golang(github.com/prometheus/common)) = 13ba4ddd0caa9c28ca7b7bffe1dfa9ed8d5ef207
Provides: bundled(golang(github.com/prometheus/procfs)) = 65c1f6f8f0fc1e2185eb9863a3bc751496404259
Provides: bundled(golang(github.com/PuerkitoBio/purell)) = v1.1.0
Provides: bundled(golang(github.com/PuerkitoBio/urlesc)) = 5bd2802263f21d8788851d5305584c82a5c75d7e
Provides: bundled(golang(github.com/renstrom/dedent)) = v1.0.0
Provides: bundled(golang(github.com/seccomp/libseccomp-golang)) = v0.9.0
Provides: bundled(golang(github.com/sirupsen/logrus)) = v1.0.0
Provides: bundled(golang(github.com/spf13/pflag)) = 9ff6c6923cfffbcd502984b8e0c80539a94968b7
Provides: bundled(golang(github.com/stretchr/testify)) = 4d4bfba8f1d1027c4fdbe371823030df51419987
Provides: bundled(golang(github.com/syndtr/gocapability)) = e7cb7fa329f456b3855136a2642b197bad7366ba
Provides: bundled(golang(github.com/tchap/go-patricia)) = v2.2.6
Provides: bundled(golang(github.com/ugorji/go)) = d23841a297e5489e787e72fceffabf9d2994b52a
Provides: bundled(golang(github.com/urfave/cli)) = 39908eb08fee7c10d842622a114a5c133fb0a3c6
Provides: bundled(golang(github.com/vbatts/tar-split)) = v0.10.2
Provides: bundled(golang(github.com/vishvananda/netlink)) = master
Provides: bundled(golang(github.com/vishvananda/netns)) = master
Provides: bundled(golang(github.com/xeipuuv/gojsonpointer)) = master
Provides: bundled(golang(github.com/xeipuuv/gojsonreference)) = master
Provides: bundled(golang(github.com/xeipuuv/gojsonschema)) = master
Provides: bundled(golang(golang.org/x/crypto)) = 3fbbcd23f1cb824e69491a5930cfeff09b12f4d2
Provides: bundled(golang(golang.org/x/net)) = c427ad74c6d7a814201695e9ffde0c5d400a7674
Provides: bundled(golang(golang.org/x/sys)) = 9aade4d3a3b7e6d876cd3823ad20ec45fc035402
Provides: bundled(golang(golang.org/x/text)) = f72d8390a633d5dfb0cc84043294db9f6c935756
Provides: bundled(golang(google.golang.org/grpc)) = v1.0.4
Provides: bundled(golang(gopkg.in/cheggaaa/pb.v1)) = v1.0.7
Provides: bundled(golang(gopkg.in/inf.v0)) = v0.9.0
Provides: bundled(golang(gopkg.in/mgo.v2)) = v2
Provides: bundled(golang(gopkg.in/yaml.v2)) = v2

%description
%{summary}
%{repo} provides a library for applications looking to use
the Container Pod concept popularized by Kubernetes.

%if %{with varlink}
%package -n python3-%{name}
BuildArch: noarch
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-varlink
Requires: python3-varlink
Provides: python3-%{name} = %{version}-%{release}
Summary: Python 3 bindings for %{name}

%description -n python3-%{name}
This package contains Python 3 bindings for %{name}.
%endif # varlink

%if 0%{?with_devel}
%package devel
Summary:       Library for applications looking to use Container Pods
BuildArch:     noarch
Provides: %{repo}-devel = %{version}-%{release}

%if 0%{?with_check} && ! 0%{?with_bundled}
BuildRequires: golang(github.com/BurntSushi/toml)
BuildRequires: golang(github.com/containerd/cgroups)
BuildRequires: golang(github.com/containernetworking/plugins/pkg/ns)
BuildRequires: golang(github.com/containers/image/copy)
BuildRequires: golang(github.com/containers/image/directory)
BuildRequires: golang(github.com/containers/image/docker)
BuildRequires: golang(github.com/containers/image/docker/archive)
BuildRequires: golang(github.com/containers/image/docker/reference)
BuildRequires: golang(github.com/containers/image/docker/tarfile)
BuildRequires: golang(github.com/containers/image/image)
BuildRequires: golang(github.com/containers/image/oci/archive)
BuildRequires: golang(github.com/containers/image/pkg/strslice)
BuildRequires: golang(github.com/containers/image/pkg/sysregistries)
BuildRequires: golang(github.com/containers/image/signature)
BuildRequires: golang(github.com/containers/image/storage)
BuildRequires: golang(github.com/containers/image/tarball)
BuildRequires: golang(github.com/containers/image/transports/alltransports)
BuildRequires: golang(github.com/containers/image/types)
BuildRequires: golang(github.com/containers/storage)
BuildRequires: golang(github.com/containers/storage/pkg/archive)
BuildRequires: golang(github.com/containers/storage/pkg/idtools)
BuildRequires: golang(github.com/containers/storage/pkg/reexec)
BuildRequires: golang(github.com/coreos/go-systemd/dbus)
BuildRequires: golang(github.com/cri-o/ocicni/pkg/ocicni)
BuildRequires: golang(github.com/docker/distribution/reference)
BuildRequires: golang(github.com/docker/docker/daemon/caps)
BuildRequires: golang(github.com/docker/docker/pkg/mount)
BuildRequires: golang(github.com/docker/docker/pkg/namesgenerator)
BuildRequires: golang(github.com/docker/docker/pkg/stringid)
BuildRequires: golang(github.com/docker/docker/pkg/system)
BuildRequires: golang(github.com/docker/docker/pkg/term)
BuildRequires: golang(github.com/docker/docker/pkg/truncindex)
BuildRequires: golang(github.com/ghodss/yaml)
BuildRequires: golang(github.com/godbus/dbus)
BuildRequires: golang(github.com/mattn/go-sqlite3)
BuildRequires: golang(github.com/mrunalp/fileutils)
BuildRequires: golang(github.com/opencontainers/go-digest)
BuildRequires: golang(github.com/opencontainers/image-spec/specs-go/v1)
BuildRequires: golang(github.com/opencontainers/runc/libcontainer)
BuildRequires: golang(github.com/opencontainers/runtime-spec/specs-go)
BuildRequires: golang(github.com/opencontainers/runtime-tools/generate)
BuildRequires: golang(github.com/opencontainers/selinux/go-selinux)
BuildRequires: golang(github.com/opencontainers/selinux/go-selinux/label)
BuildRequires: golang(github.com/pkg/errors)
BuildRequires: golang(github.com/sirupsen/logrus)
BuildRequires: golang(github.com/ulule/deepcopier)
BuildRequires: golang(golang.org/x/crypto/ssh/terminal)
BuildRequires: golang(golang.org/x/sys/unix)
BuildRequires: golang(k8s.io/apimachinery/pkg/util/wait)
BuildRequires: golang(k8s.io/client-go/tools/remotecommand)
BuildRequires: golang(k8s.io/kubernetes/pkg/kubelet/container)
%endif

Requires:      golang(github.com/BurntSushi/toml)
Requires:      golang(github.com/containerd/cgroups)
Requires:      golang(github.com/containernetworking/plugins/pkg/ns)
Requires:      golang(github.com/containers/image/copy)
Requires:      golang(github.com/containers/image/directory)
Requires:      golang(github.com/containers/image/docker)
Requires:      golang(github.com/containers/image/docker/archive)
Requires:      golang(github.com/containers/image/docker/reference)
Requires:      golang(github.com/containers/image/docker/tarfile)
Requires:      golang(github.com/containers/image/image)
Requires:      golang(github.com/containers/image/oci/archive)
Requires:      golang(github.com/containers/image/pkg/strslice)
Requires:      golang(github.com/containers/image/pkg/sysregistries)
Requires:      golang(github.com/containers/image/signature)
Requires:      golang(github.com/containers/image/storage)
Requires:      golang(github.com/containers/image/tarball)
Requires:      golang(github.com/containers/image/transports/alltransports)
Requires:      golang(github.com/containers/image/types)
Requires:      golang(github.com/containers/storage)
Requires:      golang(github.com/containers/storage/pkg/archive)
Requires:      golang(github.com/containers/storage/pkg/idtools)
Requires:      golang(github.com/containers/storage/pkg/reexec)
Requires:      golang(github.com/coreos/go-systemd/dbus)
Requires:      golang(github.com/cri-o/ocicni/pkg/ocicni)
Requires:      golang(github.com/docker/distribution/reference)
Requires:      golang(github.com/docker/docker/daemon/caps)
Requires:      golang(github.com/docker/docker/pkg/mount)
Requires:      golang(github.com/docker/docker/pkg/namesgenerator)
Requires:      golang(github.com/docker/docker/pkg/stringid)
Requires:      golang(github.com/docker/docker/pkg/system)
Requires:      golang(github.com/docker/docker/pkg/term)
Requires:      golang(github.com/docker/docker/pkg/truncindex)
Requires:      golang(github.com/ghodss/yaml)
Requires:      golang(github.com/godbus/dbus)
Requires:      golang(github.com/mattn/go-sqlite3)
Requires:      golang(github.com/mrunalp/fileutils)
Requires:      golang(github.com/opencontainers/go-digest)
Requires:      golang(github.com/opencontainers/image-spec/specs-go/v1)
Requires:      golang(github.com/opencontainers/runc/libcontainer)
Requires:      golang(github.com/opencontainers/runtime-spec/specs-go)
Requires:      golang(github.com/opencontainers/runtime-tools/generate)
Requires:      golang(github.com/opencontainers/selinux/go-selinux)
Requires:      golang(github.com/opencontainers/selinux/go-selinux/label)
Requires:      golang(github.com/pkg/errors)
Requires:      golang(github.com/sirupsen/logrus)
Requires:      golang(github.com/ulule/deepcopier)
Requires:      golang(golang.org/x/crypto/ssh/terminal)
Requires:      golang(golang.org/x/sys/unix)
Requires:      golang(k8s.io/apimachinery/pkg/util/wait)
Requires:      golang(k8s.io/client-go/tools/remotecommand)
Requires:      golang(k8s.io/kubernetes/pkg/kubelet/container)

Provides:      golang(%{import_path}/cmd/%{name}/docker) = %{version}-%{release}
Provides:      golang(%{import_path}/cmd/%{name}/formats) = %{version}-%{release}
Provides:      golang(%{import_path}/libkpod) = %{version}-%{release}
Provides:      golang(%{import_path}/libpod) = %{version}-%{release}
Provides:      golang(%{import_path}/libpod/common) = %{version}-%{release}
Provides:      golang(%{import_path}/libpod/driver) = %{version}-%{release}
Provides:      golang(%{import_path}/libpod/layers) = %{version}-%{release}
Provides:      golang(%{import_path}/pkg/annotations) = %{version}-%{release}
Provides:      golang(%{import_path}/pkg/chrootuser) = %{version}-%{release}
Provides:      golang(%{import_path}/pkg/registrar) = %{version}-%{release}
Provides:      golang(%{import_path}/pkg/storage) = %{version}-%{release}
Provides:      golang(%{import_path}/utils) = %{version}-%{release}

%description -n  libpod-devel
%{summary}

This package contains library source intended for
building other packages which use import path with
%{import_path} prefix.
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%package unit-test-devel
Summary:         Unit tests for %{name} package
%if 0%{?with_check}
#Here comes all BuildRequires: PACKAGE the unit tests
#in %%check section need for running
%endif

# test subpackage tests code from devel subpackage
Requires:        %{name}-devel = %{version}-%{release}

%if 0%{?with_check} && ! 0%{?with_bundled}
BuildRequires: golang(github.com/stretchr/testify/assert)
BuildRequires: golang(github.com/urfave/cli)
%endif

Requires:      golang(github.com/stretchr/testify/assert)
Requires:      golang(github.com/urfave/cli)

%description unit-test-devel
%{summary}
libpod provides a library for applications looking to use the Container Pod concept popularized by Kubernetes.

This package contains unit tests for project
providing packages with %{import_path} prefix.
%endif

%prep
%autosetup -Sgit -n %{repo}-%{commit0}
sed -i '/\/bin\/env/d' completions/bash/%{name}
mv pkg/hooks/README.md pkg/hooks/README-hooks.md

%build
mkdir _build
pushd _build
mkdir -p src/%{provider}.%{provider_tld}/%{project}
ln -s ../../../../ src/%{import_path}
popd
ln -s vendor src
export GOPATH=$(pwd)/_build:$(pwd):$(pwd):%{gopath}
export BUILDTAGS="selinux seccomp $(hack/btrfs_installed_tag.sh) $(hack/btrfs_tag.sh) $(hack/libdm_tag.sh) containers_image_ostree_stub"

GOPATH=$GOPATH go generate ./cmd/podman/varlink/...
GOPATH=$GOPATH BUILDTAGS=$BUILDTAGS %gobuild -o bin/%{name} %{import_path}/cmd/%{name}
BUILDTAGS=$BUILDTAGS make %{name} docs

%if %{with varlink}
BUILDTAGS=$BUILDTAGS make varlink_generate python-%{name}

#untar contents for python-podman
pushd contrib/python/dist
tar zxf %{name}*.tar.gz
popd
%endif # varlink

%install
install -dp %{buildroot}%{_unitdir}
%make_install PREFIX=%{buildroot}%{_prefix} install install.completions

%if %{with varlink}
#install python-podman
pushd contrib/python
%{__python3} setup.py install --root %{buildroot}
popd
%endif # varlink

# install libpod.conf
install -dp %{buildroot}%{_datadir}/containers
install -p -m 644 %{repo}.conf %{buildroot}%{_datadir}/containers

# source codes for building projects
%if 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/

echo "%%dir %%{gopath}/src/%%{import_path}/." >> devel.file-list
# find all *.go but no *_test.go files and generate devel.file-list
for file in $(find . \( -iname "*.go" -or -iname "*.s" \) \! -iname "*_test.go" | grep -v "vendor") ; do
    dirprefix=$(dirname $file)
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$dirprefix
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> devel.file-list

    while [ "$dirprefix" != "." ]; do
        echo "%%dir %%{gopath}/src/%%{import_path}/$dirprefix" >> devel.file-list
        dirprefix=$(dirname $dirprefix)
    done
done
%endif

# testing files for this project
%if 0%{?with_unit_test} && 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
# find all *_test.go files and generate unit-test-devel.file-list
for file in $(find . -iname "*_test.go" | grep -v "vendor") ; do
    dirprefix=$(dirname $file)
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$dirprefix
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> unit-test-devel.file-list

    while [ "$dirprefix" != "." ]; do
        echo "%%dir %%{gopath}/src/%%{import_path}/$dirprefix" >> devel.file-list
        dirprefix=$(dirname $dirprefix)
    done
done
%endif

%if 0%{?with_devel}
sort -u -o devel.file-list devel.file-list
%endif

%check
%if 0%{?with_check} && 0%{?with_unit_test} && 0%{?with_devel}
%if ! 0%{?with_bundled}
export GOPATH=%{buildroot}/%{gopath}:%{gopath}
%else
# Since we aren't packaging up the vendor directory we need to link
# back to it somehow. Hack it up so that we can add the vendor
# directory from BUILD dir as a gopath to be searched when executing
# tests from the BUILDROOT dir.
ln -s ./ ./vendor/src # ./vendor/src -> ./vendor

export GOPATH=%{buildroot}/%{gopath}:$(pwd)/vendor:%{gopath}
%endif

%if ! 0%{?gotest:1}
%global gotest go test
%endif
        
%gotest %{import_path}/cmd/%{name}
%gotest %{import_path}/libkpod
%gotest %{import_path}/libpod
%gotest %{import_path}/pkg/registrar
%endif

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files
%license LICENSE
%doc README.md CONTRIBUTING.md pkg/hooks/README-hooks.md install.md code-of-conduct.md transfer.md
%{_bindir}/%{name}
%{_mandir}/man1/*.1*
%{_mandir}/man5/*.5*
%{_datadir}/bash-completion/completions/*
%config(noreplace) %{_sysconfdir}/cni/net.d/87-%{name}-bridge.conflist
%{_datadir}/containers/%{repo}.conf
%{_unitdir}/io.%{project}.%{name}.service
%{_unitdir}/io.%{project}.%{name}.socket
%{_prefix}/lib/tmpfiles.d/%{name}.conf

%if %{with varlink}
%files -n python3-%{name}
%license LICENSE
%doc README.md CONTRIBUTING.md pkg/hooks/README-hooks.md install.md code-of-conduct.md transfer.md
%dir %{python3_sitelib}
%{python3_sitelib}/*
%endif # varlink

%if 0%{?with_devel}
%files -n libpod-devel -f devel.file-list
%license LICENSE
%doc README.md CONTRIBUTING.md pkg/hooks/README-hooks.md install.md code-of-conduct.md transfer.md
%dir %{gopath}/src/%{provider}.%{provider_tld}/%{project}
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%files unit-test-devel -f unit-test-devel.file-list
%license LICENSE
%doc README.md CONTRIBUTING.md pkg/hooks/README-hooks.md install.md code-of-conduct.md transfer.md
%endif

%changelog
* Tue Jun 26 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.5-3.git208b9a6
- autobuilt 208b9a6

* Mon Jun 25 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.5-2.gite89bbd6
- autobuilt e89bbd6

* Sat Jun 23 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.5-1.git7182339
- bump to 0.6.5
- autobuilt 7182339

* Fri Jun 22 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.4-7.git4bd0f22
- autobuilt 4bd0f22

* Thu Jun 21 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.4-6.git6804fde
- autobuilt 6804fde

* Wed Jun 20 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.4-5.gitf228cf7
- autobuilt f228cf7

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.6.4-4.git5645789
- Rebuilt for Python 3.7

* Tue Jun 19 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.4-3.git5645789
- autobuilt 5645789

* Mon Jun 18 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.4-2.git9e13457
- autobuilt 9e13457

* Sat Jun 16 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.4-1.gitb43677c
- bump to 0.6.4
- autobuilt b43677c

* Fri Jun 15 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.3-6.git6bdf023
- autobuilt 6bdf023

* Thu Jun 14 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.3-5.git65033b5
- autobuilt 65033b5

* Wed Jun 13 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.3-4.git95ea3d4
- autobuilt 95ea3d4

* Tue Jun 12 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.3-3.gitab72130
- autobuilt ab72130

* Mon Jun 11 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.3-2.git1e9e530
- autobuilt 1e9e530

* Sat Jun 09 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.3-1.gitb78e7e4
- bump to 0.6.3
- autobuilt b78e7e4

* Fri Jun 08 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.2-7.git1cbce85
- autobuilt 1cbce85

* Thu Jun 07 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.2-6.gitb1ebad9
- autobuilt b1ebad9

* Wed Jun 06 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.2-5.git7b2b2bc
- autobuilt 7b2b2bc

* Tue Jun 05 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.2-4.git14cf6d2
- autobuilt 14cf6d2

* Mon Jun 04 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.2-3.gitcae49fc
- autobuilt cae49fc

* Sun Jun 03 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.2-2.git13f7450
- autobuilt 13f7450

* Sat Jun 02 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.2-1.git22e6f11
- bump to 0.6.2
- autobuilt 22e6f11

* Fri Jun 01 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.1-4.gita9e9fd4
- autobuilt a9e9fd4

* Thu May 31 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.1-3.gita127b4f
- autobuilt a127b4f

* Wed May 30 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.1-2.git8ee0f2b
- autobuilt 8ee0f2b

* Sat May 26 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.1-1.git44d1c1c
- bump to 0.6.1
- autobuilt 44d1c1c

* Fri May 18 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.5.3-7.gitc54b423
- make python3-podman the same version as the main package
- build python3-podman only for fedora >= 28

* Fri May 18 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.5.3-6.gitc54b423
- autobuilt c54b423

* Wed May 16 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.5.3-5.git624660c
- built commit 624660c
- New subapackage: python3-podman

* Wed May 16 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.5.3-4.git9fcc475
- autobuilt 9fcc475

* Wed May 16 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.5.3-3.git0613844
- autobuilt 0613844

* Tue May 15 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.5.3-2.git45838b9
- autobuilt 45838b9

* Fri May 11 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.5.3-1.git07253fc
- bump to v0.5.3
- built commit 07253fc

* Fri May 11 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.5.2-5.gitcc1bad8
- autobuilt cc1bad8

* Wed May 09 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.5.2-4.git2526355
- autobuilt 2526355

* Tue May 08 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.5.2-3.gitfaa8c3e
- autobuilt faa8c3e

* Sun May 06 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.5.2-2.gitfa4705c
- autobuilt fa4705c

* Sat May 05 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.5.2-1.gitbb0e754
- bump to 0.5.2
- autobuilt bb0e754

* Fri May 04 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.5.1-5.git5ae940a
- autobuilt 5ae940a

* Wed May 02 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.5.1-4.git64dc803
- autobuilt commit 64dc803

* Wed May 02 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.5.1-3.git970eaf0
- autobuilt commit 970eaf0

* Tue May 01 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.5.1-2.git7a0a855
- autobuilt commit 7a0a855

* Sun Apr 29 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.5.1-1.giteda0fd7
- reflect version number correctly
- my builder script error ended up picking the wrong version number previously

* Sun Apr 29 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-5.giteda0fd7
- autobuilt commit eda0fd7

* Sat Apr 28 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-4.git6774425
- autobuilt commit 6774425

* Fri Apr 27 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-3.git39a7a77
- autobuilt commit 39a7a77

* Thu Apr 26 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-2.git58cb8f7
- autobuilt commit 58cb8f7

* Wed Apr 25 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-1.gitbef93de
- bump to 0.4.2
- autobuilt commit bef93de

* Tue Apr 24 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.4.4-1.git398133e
- use correct version number

* Tue Apr 24 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-22.git398133e
- autobuilt commit 398133e

* Sun Apr 22 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-21.gitcf1d884
- autobuilt commit cf1d884

* Fri Apr 20 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-20.git9b457e3
- autobuilt commit 9b457e3

* Fri Apr 20 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-1.gitbef93de9.git228732d
- autobuilt commit 228732d

* Thu Apr 19 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-1.gitbef93de8.gitf2658ec
- autobuilt commit f2658ec

* Thu Apr 19 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-1.gitbef93de7.git6a9dbf3
- autobuilt commit 6a9dbf3

* Tue Apr 17 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-1.gitbef93de6.git96d1162
- autobuilt commit 96d1162

* Tue Apr 17 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-1.gitbef93de5.git96d1162
- autobuilt commit 96d1162

* Mon Apr 16 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-1.gitbef93de4.git6c5ebb0
- autobuilt commit 6c5ebb0

* Mon Apr 16 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-1.gitbef93de3.gitfa8442e
- autobuilt commit fa8442e

* Mon Apr 16 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-1.gitbef93de2.gitfa8442e
- autobuilt commit fa8442e

* Sun Apr 15 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-1.gitbef93de1.gitfa8442e
- autobuilt commit fa8442e

* Sat Apr 14 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-1.gitbef93de0.git62b59df
- autobuilt commit 62b59df

* Fri Apr 13 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-9.git191da31
- autobuilt commit 191da31

* Thu Apr 12 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-8.git6f51a5b
- autobuilt commit 6f51a5b

* Wed Apr 11 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-7.git77a1665
- autobuilt commit 77a1665

* Tue Apr 10 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-6.git864b9c0
- autobuilt commit 864b9c0

* Tue Apr 10 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-5.git864b9c0
- autobuilt commit 864b9c0

* Tue Apr 10 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-4.git998fd2e
- autobuilt commit 998fd2e

* Sun Apr 08 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-3.git998fd2e
- autobuilt commit 998fd2e

* Sun Apr 08 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.4.2-2.git998fd2e
- autobuilt commit 998fd2e

* Sun Apr 08 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.4.2-1.gitbef93de.git998fd2e
- bump to 0.4.2
- autobuilt commit 998fd2e

* Thu Mar 29 2018 baude <bbaude@redhat.com> - 0.3.5-2.gitdb6bf9e3
- Upstream release 0.3.5

* Tue Mar 27 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.3.5-1.git304bf53
- built commit 304bf53

* Fri Mar 23 2018 baude <bbaude@redhat.com> - 0.3.4-1.git57b403e
- Upstream release 0.3.4

* Fri Mar 16 2018 baude <bbaude@redhat.com> - 0.3.3-2.dev.gitbc358eb
- Upstream release 0.3.3

* Wed Mar 14 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.3.3-1.dev.gitbc358eb
- built podman commit bc358eb
- built conmon from cri-o commit 712f3b8

* Fri Mar 09 2018 baude <bbaude@redhat.com> - 0.3.2-1.gitf79a39a
- Release 0.3.2-1

* Sun Mar 04 2018 baude <bbaude@redhat.com> - 0.3.1-2.git98b95ff
- Correct RPM version

* Fri Mar 02 2018 baude <bbaude@redhat.com> - 0.3.1-1-gitc187538
- Release 0.3.1-1

* Sun Feb 25 2018 Peter Robinson <pbrobinson@fedoraproject.org> 0.2.2-2.git525e3b1
- Build on ARMv7 too (Fedora supports containers on that arch too)

* Fri Feb 23 2018 baude <bbaude@redhat.com> - 0.2.2-1.git525e3b1
- Release 0.2.2

* Fri Feb 16 2018 baude <bbaude@redhat.com> - 0.2.1-1.git3d0100b
- Release 0.2.1

* Wed Feb 14 2018 baude <bbaude@redhat.com> - 0.2-3.git3d0100b
- Add dep for atomic-registries

* Tue Feb 13 2018 baude <bbaude@redhat.com> - 0.2-2.git3d0100b
- Add more 64bit arches
- Add containernetworking-cni dependancy
- Add iptables dependancy

* Mon Feb 12 2018 baude <bbaude@redhat.com> - 0-2.1.git3d0100
- Release 0.2

* Tue Feb 06 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0-0.3.git367213a
- Resolves: #1541554 - first official build
- built commit 367213a

* Fri Feb 02 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0-0.2.git0387f69
- built commit 0387f69

* Wed Jan 10 2018 Frantisek Kluknavsky <fkluknav@redhat.com> - 0-0.1.gitc1b2278
- First package for Fedora


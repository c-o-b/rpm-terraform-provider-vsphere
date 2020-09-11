%global	owner	terraform-providers
%global	proj	vsphere
%global	repo	terraform-provider-%{proj}
%global	host	github.com
%global	archive	v%{version}.tar.gz
%global	dir	%{repo}-%{version}
%global	namespace github.com/%{owner}/%{repo}
%global	v13base	%{_datadir}/terraform/plugins/%{regsite}/%{regorg}/%{proj}/%{version}/%{regos}_%{regarch}

%global	regsite	registry.terraform.io
%global	regorg	hashicorp
%global	regarch	amd64
%global	regos	%{_target_os}

%global	version	1.14.0
%global	release	2.2

# emulate mock bubblewrap dependency; delete with proper source
%if %{?rhel:0}%{!?rhel:1}
%global rhel	%(rpm -qf --qf "%{version}" /etc/issue)
%endif
%if %{?dist:0}%{!?dist:1}
%global dist	el%{?rhel}%{!?rhel:0}
%endif


# Actually, don't strip at all since we are not even building debug packages
%define	__strip /bin/true
%global	debug_package	%{nil}

Name:		golang-github-%{repo}
%global	summary	Terraform provider for vSphere
Summary:	%{summary}

Version:	%{version}
Release:	%{release}
Epoch:		0

Group:		Applications/System
License:	MPL2; info@terraform.io

URL:		https://%{host}/%{owner}/%{repo}
Source0:	%{url}/archive/%{archive}

BuildRequires: golang make
BuildRequires: golang(github.com/Sirupsen/logrus)
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Terraform provider for vSphere


%package v12
Summary:	%{summary} for v12
Group:		%{group}
%description v12
This package works with terraform up to v0.12
Requires:	terraform < 0.13.0
Provides:	%{repo}
Obsoletes:	%{name}


%package	v13
Summary:	%{summary} for v13+
Group:		%{group}
%description v13
This package works with Terraform 'minor' release 0.13 and up
Requires:	terraform >= 0.13.0
Provides:	%{repo}
Obsoletes:	%{name}


%prep
%setup -q -n %{dir}

%build
export GOPATH=$PWD
export GOOS=%{_target_os}
export GOARCH=%{regarch}
#export GOFLAGS=-modcacherw
mkdir -p src/%{namespace}/

shopt -s extglob dotglob
mv !(src) src/%{namespace}/
shopt -u extglob dotglob
pushd src/%{namespace}/
#go get %{namespace}/something
#go get github.com/Sirupsen/logrus

make build
popd

%install
[ "%{buildroot}" = "/" ] || [ ! -d %{buildroot} ] || rm -rf %{buildroot}
install -d -m 755 %{buildroot}
%{__mkdir_p} \
	-m 755 \
	%{buildroot}%{v13base} \
	%{buildroot}%{_bindir}

# install binary
%{__install} \
	bin/%{repo} \
	%{buildroot}%{v13base}/

ln \
	%{buildroot}%{v13base}/%{repo} \
	%{buildroot}%{_bindir}/


%clean
[ "%{buildroot}" = "/" ] || [ ! -d %{buildroot} ] || rm -rf %{buildroot}

%files	v12
%defattr(-,root,root,-)
#doc AUTHORS COPYING ChangeLog NEWS README TODO
%{_bindir}/*

%files	v13
%defattr(-,root,root,-)
#doc AUTHORS COPYING ChangeLog NEWS README TODO
%{v13base}/*

# %(date +"%a %b %d %Y") $Author: build $ %{version}-%{release}
%changelog
* Thu Sep 10 2020 Bishop Clark <bishopolis@gmail.com> - 1.14.0-2.2
- issue with the summary macro

* Thu Sep 10 2020 Bishop Clark <bishopolis@gmail.com> - 1.14.0-2.1
- obsolete the older package

* Sun Sep 06 2020 Bishop Clark <bishopolis@gmail.com> - 1.14.0-2.0
- build sub-packages fro both (incompatible) desployments \sigh #GoLF

* Thu Sep 03 2020 Bishop Clark <bishopolis@gmail.com> - 1.14.0-1.1
- fix deps 

* Wed Sep 02 2020 Bishop Clark <bishopolis@gmail.com> - 1.14.0-1.0
- redo deployment directory from stackoverflow.com/questions/63680319

* Fri Jan 17 2020 Bishop Clark <bishopolis@gmail.com> - 1.14.0-0.1
- Initial build

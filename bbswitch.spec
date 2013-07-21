#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_with	verbose		# verbose build (V=1)

# nothing to be placed to debuginfo package
%define		_enable_debug_packages	0

%define		rel	1
%define		modname	bbswitch
Summary:	Disable discrete graphics (currently nvidia only)
Name:		%{modname}%{_alt_kernel}
Version:	0.7
Release:	%{rel}
License:	GPL v2+
URL:		https://github.com/Bumblebee-Project/bbswitch
Source0:	https://github.com/Bumblebee-Project/bbswitch/archive/v%{version}.tar.gz?/%{modname}-%{version}.tgz
# Source0-md5:	b9df5ea40109ef9766448a0577c798e6
Group:		Base/Kernel
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRequires:	rpmbuild(macros) >= 1.379
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Disable discrete graphics (currently nvidia only).

%package -n kernel%{_alt_kernel}-misc-%{modname}
Summary:	Disable discrete graphics (currently nvidia only)
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif

%description -n kernel%{_alt_kernel}-misc-%{modname}
Disable discrete graphics (currently nvidia only).

%prep
%setup -qn %{modname}-%{version}

%build
%if %{with kernel}
%build_kernel_modules -m %{modname}
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with kernel}
%install_kernel_modules -m %{modname} -d misc
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-misc-%{modname}
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-misc-%{modname}
%depmod %{_kernel_ver}

%if %{with kernel}
%files -n kernel%{_alt_kernel}-misc-%{modname}
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/*.ko*
%endif

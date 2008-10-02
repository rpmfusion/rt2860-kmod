# buildforkernels macro hint: when you build a new version or a new release
# that contains bugfixes or other improvements then you must disable the
# "buildforkernels newest" macro for just that build; immediately after
# queuing that build enable the macro again for subsequent builds; that way
# a new akmod package will only get build when a new one is actually needed
%define buildforkernels newest

%define SourceDir 2008_0708_RT2860_Linux_STA_v1.7.0.0
%define _default_patch_fuzz 2

Name:           rt2860-kmod
Version:        1.7.0
Release:        5%{?dist}.1
Summary:        Kernel module for RaLink 802.11 wireless devices rt2760/rt2790/rt2860/rt2890

Group:          System Environment/Kernel
License:        GPLv2+
URL:            http://www.ralinktech.com/
Source0:        http://www.ralinktech.com.tw/data/drivers/%{SourceDir}.tar.bz2
Source11:       rt2860-kmodtool-excludekernel-filterfile
Patch0:         rt2860-remove-tftpboot-copy.patch
Patch1:         rt2860-add-network-mgr-support.diff
Patch2:         rt2860-dat-install-fixes.patch
Patch3:         rt2860-2.6.25-iwe_stream-fix.diff
Patch4:         rt2860-net-namespace-separation.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# needed for plague to make sure it builds for i586 and i686
ExclusiveArch:  i586 i686 x86_64 ppc

# get the needed BuildRequires (in parts depending on what we build for)
BuildRequires:  %{_bindir}/kmodtool
%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }
# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} --filterfile %{SOURCE11} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
This package contains the Ralink Driver for WiFi, a linux device
driver for 802.11a/b/g universal NIC cards - either PCI, PCIe or
MiniPCI - that use Ralink chipsets (rt2760, rt2790, rt2860, rt2890).

%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}
# print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu}  --repo rpmfusion --kmodname %{name} --filterfile %{SOURCE11} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null
%setup -q -c -T -a 0
(cd %{SourceDir} ; 
%patch0 -p1 -b .tftpboot
%patch1 -p1 -b .network-mgr
%patch2 -p1 -b .dat-install
%patch3 -p1 -b .2.6.25.fixes
%patch4 -p1 -b .patch
)
for kernel_version  in %{?kernel_versions} ; do
    cp -a %{SourceDir} _kmod_build_${kernel_version%%___*}
done


%build
for kernel_version  in %{?kernel_versions} ; do
    pushd _kmod_build_${kernel_version%%___*}
    make LINUX_SRC="${kernel_version##*___}"
    popd
done


%install
rm -rf $RPM_BUILD_ROOT
for kernel_version  in %{?kernel_versions} ; do
    make -C _kmod_build_${kernel_version%%___*} LINUX_SRC="${kernel_version##*___}"  LINUX_SRC_MODULE=$RPM_BUILD_ROOT/%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix} DAT_PREFIX=$RPM_BUILD_ROOT install
done

# allow stripping:
chmod 0755 $RPM_BUILD_ROOT/%{kmodinstdir_prefix}/*/%{kmodinstdir_postfix}/* || :
# file is part of the common package:
rm -fr $RPM_BUILD_ROOT/etc || :
# akmods:
%{?akmod_install}


%clean
rm -rf $RPM_BUILD_ROOT


%changelog
* Tue Oct 02 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 1.7.0-5
- rebuild for RPM Fusion

* Sun Sep 21 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 1.7.0-4
- _default_patch_fuzz 2 for new rpm
- make some comments in install section not fail when building akmod package

* Fri Sep 14 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 1.7.0-3
- add rt2860-net-namespace-separation.patch to make it compile with 2.6.26.3
  from Fedora; patch provided by James as text in #2083
- License is GPLv2+ 

* Fri Sep 05 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 1.7.0-2
- some small fixes and cleanups

* Fri Aug 29 2008 James Bottomley <James.Bottomley [AT] hansenpartnership [DOT] com> 1.7.0-1
- Initial Version
- Applied patch to fix up around iwe_mark interface changes

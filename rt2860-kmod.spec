# buildforkernels macro hint: when you build a new version or a new release
# that contains bugfixes or other improvements then you must disable the
# "buildforkernels newest" macro for just that build; immediately after
# queuing that build enable the macro again for subsequent builds; that way
# a new akmod package will only get build when a new one is actually needed
%define buildforkernels newest

Name:		rt2860-kmod
Version:	2.1.1.0
Release:	1%{?dist}.2
Summary:	Kernel module for RaLink 802.11 wireless devices rt2760/rt2790/rt2860/rt2890

Group:		System Environment/Kernel
License:	GPLv2+
URL:		http://www.ralinktech.com/ralink/Home/Support/Linux.html
Source0:	http://www.ralinktech.com.tw/data/drivers/2009_0424_RT2860_Linux_STA_V%{version}.tgz
Source11:	rt2860-kmodtool-excludekernel-filterfile

Patch1:		rt2860-dat-install-fixes.patch
Patch2:		rt2860-add-network-mgr-support.diff
Patch3:		rt2860-remove-tftpboot-copy.patch
Patch4:		rt2860-no2.4-in-kernelversion.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	%{_bindir}/kmodtool

# needed for plague to make sure it builds for i586 and i686
ExclusiveArch:	i586 i686 x86_64 ppc ppc64

%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} --filterfile %{SOURCE11} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
This package contains the Ralink Driver for WiFi, a linux device
driver for 802.11a/b/g universal NIC cards - either PCI, PCIe or
MiniPCI - that use Ralink chipsets (rt2760, rt2790, rt2860, rt2890).

%prep
%{?kmodtool_check}

# print kmodtool output for debugging purposes:
kmodtool --target %{_target_cpu}  --repo rpmfusion --kmodname %{name} --filterfile %{SOURCE11} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%setup -q -c -T -a 0

pushd *RT2860*Linux*STA*
%patch1 -p1 -b .rpmbuild
%patch2 -p1 -b .NetworkManager
%patch3 -p1 -b .tftpboot
%patch4 -p1 -b .no24
popd

# Fix weird permissions
find . -name "*.c" -exec chmod -x {} \;
find . -name "*.h" -exec chmod -x {} \;

for kernel_version in %{?kernel_versions} ; do
 cp -a *RT2860*Linux*STA* _kmod_build_${kernel_version%%___*}
done

%build
for kernel_version in %{?kernel_versions}; do
 make -C _kmod_build_${kernel_version%%___*} LINUX_SRC="${kernel_version##*___}"
done

%install
rm -rf ${RPM_BUILD_ROOT}
for kernel_version in %{?kernel_versions}; do
 make -C _kmod_build_${kernel_version%%___*} KERNELPATH="${kernel_version##*___}" KERNELRELEASE="${kernel_version%%___*}" INST_DIR=${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix} install
done

chmod 0755 $RPM_BUILD_ROOT/%{kmodinstdir_prefix}/*/%{kmodinstdir_postfix}/*
%{?akmod_install}

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Tue May 12 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.1.0-1.2
- rebuild for new kernels

* Fri May 08 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.1.0-1.1
- rebuild for new kernels

* Sun Apr 26 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 2.1.1.0-1
- version update (2.1.1.0)

* Mon Apr 20 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 2.1.0.0-1
- version update (2.1.0.0)

* Thu Mar 26 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.8.0.0-1.14
- Bugfix: kmod doesn't compile when the kernel version has a "2.4" substring
- Add 2.6.29 compilation patch (just in case)

* Wed Mar 25 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.8.0.0-1.13
- rebuild for new kernels

* Thu Feb 26 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.8.0.0-1.12
- rebuild for latest Fedora kernel;

* Fri Feb 13 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.8.0.0-1.11
- rebuild for latest Fedora kernel;

* Wed Jan 21 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.8.0.0-1.10
- rebuild for latest Fedora kernel;

* Sat Dec 20 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.8.0.0-1.9
- rebuild for latest Fedora kernel;

* Tue Dec 02 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.8.0.0-1.8
- rebuild for latest Fedora kernel;

* Wed Nov 19 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.8.0.0-1.7
- rebuild for latest Fedora kernel;

* Fri Nov 14 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.8.0.0-1.6
- rebuild for latest Fedora kernel;

* Wed Nov 12 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.8.0.0-1.5
- rebuild for latest Fedora kernel;

* Fri Nov 07 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.8.0.0-1.4
- rebuild for latest Fedora kernel;

* Thu Nov 06 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.8.0.0-1.3
- rebuild for latest Fedora kernel;

* Thu Oct 23 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.8.0.0-1.2
- rebuild for latest kernel; enable ppc again

* Sun Oct 19 2008 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com>  1.8.0.0-1.1
- update strip-tftpboot-copy.patch to match rt2860 sources with no fuzziness
- revert the patch names to the old versions

* Sun Oct 19 2008 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com>  1.8.0.0-1
- version update (1.8.0.0)
- patches taken from rt2870-kmod directly

* Tue Oct 02 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 1.7.0-6.1
- disable ppc ppc64; both fail

* Tue Oct 02 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 1.7.0-5.1
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

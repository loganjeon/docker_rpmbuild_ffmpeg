# DO NOT CREATE DEBUG PACKAGE
%global _enable_debug_package 0
%global debug_package %{nil}

%define RPMNAME ffmpeg
%define VERSION 4.0.1

Name: %{RPMNAME}
Version: %{VERSION}
Release: 1%{?dist}
Summary: ffmpeg for SDBD on centos:7.2.1511

Group: tview
License: SK Telecom
URL: http://www.sktelecom.com
Source0: %{RPMNAME}-%{VERSION}.tar.gz
BuildRoot: %{_tmppath}/%{name}-root

Provides: ffmpeg = %{version}-%{release}

BuildRequires: yasm
Requires: %{name}-libs = %{version}-%{release}

%package libs
Summary:        Library for ffmpeg
Group: System Environment/Libraries

%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires: %{name}-libs = %{version}-%{release}

%description
%{RPMNAME}-%{VERSION}
ffmpeg for converting Raw stream file to muxed media file(avi or mp4)

%description devel
This package contains development files for ffmpeg

%description libs
This package contains the libraries for ffmpeg


%prep
%setup -q -n %{name}-%{version}
test -f version.h || echo "#define FFMPEG_VERSION \"%{evr}\"" > version.h

%build
./configure --prefix=%{_prefix} --libdir=%{_libdir} \
			--shlibdir=%{_libdir} --mandir=%{_mandir} \
			--disable-stripping
make
# remove some zero-length files, ...
pushd doc
rm -f general.html.d platform.html.d git-howto.html.d \
	      developer.html.d texi2pod.pl faq.html.d
popd

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} incdir=%{buildroot}%{_includedir}/ffmpeg
# Remove from the included docs
rm -f doc/Makefile
rm -f %{buildroot}/usr/share/doc/ffmpeg/*.html

%clean
rm -rf %{buildroot}

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING* CREDITS README* MAINTAINERS LICENSE* RELEASE doc/ RELEASE_NOTES VERSION
%{_bindir}/*
%{_datadir}/ffmpeg
%{_mandir}/man1/*

%files libs
%defattr(-,root,root,-)
%doc COPYING* CREDITS README* MAINTAINERS LICENSE* RELEASE doc/ RELEASE_NOTES VERSION
%{_libdir}/*.a
%{_mandir}/man3/*

%files devel
%defattr(-,root,root,-)
%doc COPYING* CREDITS README* MAINTAINERS LICENSE* RELEASE doc/ RELEASE_NOTES VERSION
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc


%changelog
* Wed Jun 20 2018 Yeonggyoo Jeon <yg.jeon@sk.com> - 4.0.1
RPM Pakaging ffmpeg-4.0.1 version.

* Thu Jun 14 2018 Michael Niedermayer <michael@niedermayer.cc> - 4.0.1
avcodec/aacdec_fixed: Fix undefined integer overflow in apply_independent_coupling_fixed()
Fixes: signed integer overflow: 1195517 * 2048 cannot be represented in type 'int'
Fixes: 8636/clusterfuzz-testcase-minimized-ffmpeg_AV_CODEC_ID_AAC_FIXED_fuzzer-4695836326887424

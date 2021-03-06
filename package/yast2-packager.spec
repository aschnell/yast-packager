#
# spec file for package yast2-packager
#
# Copyright (c) 2018 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


Name:           yast2-packager
Version:        4.2.1
Release:        0

BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Source0:        %{name}-%{version}.tar.bz2

Url:            https://github.com/yast/yast-packager
BuildRequires:  update-desktop-files
BuildRequires:  yast2-devtools >= 3.1.10
BuildRequires:  rubygem(%{rb_default_ruby_abi}:cfa) >= 0.5.0
BuildRequires:  rubygem(%{rb_default_ruby_abi}:rspec)
BuildRequires:  rubygem(%{rb_default_ruby_abi}:yast-rake)

# Y2Storage::Device#exists_in_raw_probed
BuildRequires:  yast2-storage-ng >= 4.0.141
# break the yast2-packager -> yast2-storage-ng -> yast2-packager build cycle
#!BuildIgnore: yast2-packager

# Y2Packager::ProductLicense
BuildRequires:  yast2 >= 4.0.63

# Pkg::PrdLicenseLocales
BuildRequires:  yast2-pkg-bindings >= 4.0.8

# Augeas lenses
BuildRequires:  augeas-lenses

# Newly added RPM
Requires:       yast2-country-data >= 2.16.3

# Pkg::PrdLicenseLocales
Requires:       yast2-pkg-bindings >= 4.0.8

# Y2Packager::ProductLicense
Requires:       yast2 >= 4.0.63

# unzipping license file
Requires:       unzip

# HTTP, FTP, HTTPS modules (inst_productsources.ycp)
Requires:       yast2-transfer

# XML module (inst_productsources.ycp)
Requires:       yast2-xml

# Bugzilla #305503 - storing/checking MD5 of licenses
Requires:       /usr/bin/md5sum

# .process agent
Requires:       yast2-core >= 2.16.35

# Y2Storage::Device#exists_in_raw_probed
Requires:       yast2-storage-ng >= 4.0.141

# Augeas lenses
Requires:       augeas-lenses

# zypp.conf model and minimal modifications (bsc#1023204)
Requires:       rubygem(%{rb_default_ruby_abi}:cfa) >= 0.5.0

# setenv() builtin
Conflicts:      yast2-core < 2.15.10

# NotEnoughMemory-related functions moved to misc.ycp import-file
Conflicts:      yast2-add-on < 2.15.15

# One of libyui-qt-pkg, libyui-ncurses-pkg, libyui-gtk-pkg
Requires:       libyui_pkg

# ensure that 'checkmedia' is on the medium
Recommends:     checkmedia

# for registering media add-ons on SLE
# (openSUSE does not contain the registration module)
%if 0%{?sles_version}
Recommends:     yast2-registration
%endif

# force *-webpin subpackage removal at upgrade
Obsoletes:      yast2-packager-devel-doc
Obsoletes:      yast2-packager-webpin < %version

Requires:       yast2-ruby-bindings >= 1.0.0
Summary:        YaST2 - Package Library
License:        GPL-2.0-or-later
Group:          System/YaST

%description
This package contains the libraries and modules for software management.

%prep
%setup -n %{name}-%{version}

%check
rake test:unit

%build

%install
rake install DESTDIR="%{buildroot}"

%suse_update_desktop_file yast2-packager

%post
%desktop_database_post

%postun
%desktop_database_postun

%files
%defattr(-,root,root)
%dir %{yast_yncludedir}/checkmedia
%dir %{yast_yncludedir}/packager
%dir %{yast_libdir}/packager
%dir %{yast_libdir}/packager/cfa
%dir %{yast_libdir}/y2packager
%dir %{yast_ybindir}
%{yast_ybindir}/*
%{yast_yncludedir}/checkmedia/*
%{yast_yncludedir}/packager/*
%{yast_libdir}/packager/*
%{yast_libdir}/packager/cfa/*
%{yast_libdir}/y2packager/*
%{yast_clientdir}/*.rb
%{yast_moduledir}/*
%{yast_desktopdir}/*.desktop
%{_datadir}/applications/*.desktop
%{yast_scrconfdir}/*
%{yast_execcompdir}/servers_non_y2/ag_*
%{yast_icondir}
%dir %{yast_docdir}
%license COPYING
%doc %{yast_docdir}/README.md
%doc %{yast_docdir}/CONTRIBUTING.md

%changelog

# TODO
# - use system libev (0.5.0 bundles libev 4.15)
#
# Conditional build:
%bcond_with	tests		# build without tests

%define	pkgname	nio4r
Summary:	NIO provides a high performance selector API for monitoring IO objects
Name:		ruby-%{pkgname}
Version:	0.5.0
Release:	3
License:	MIT
Group:		Development/Languages
Source0:	http://rubygems.org/downloads/%{pkgname}-%{version}.gem
# Source0-md5:	c00295b39521d713d0eddb0925f4147d
URL:		https://github.com/celluloid/nio4r
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.665
BuildRequires:	ruby-devel
%if %{with tests}
BuildRequires:	ruby-rake
BuildRequires:	ruby-rake-compiler
BuildRequires:	ruby-rspec
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
When it comes to managing many IO objects on Ruby, there aren't a
whole lot of options. The most powerful API Ruby itself gives you is
Kernel.select, and select is hurting when it comes to performance and
in terms of having a nice API.

Once upon a time Java was a similar mess. They got out of it by adding
the Java NIO API. Java NIO provides a high performance selector API
for monitoring large numbers of file descriptors.

This library aims to incorporate the ideas of Java NIO in Ruby. These
are:
- Expose high level interfaces for doing high performance IO, but keep
  the codebase small to encourage multiple implementations on different
  platforms
- Be as portable as possible, in this case across several Ruby VMs
- Provide inherently thread-safe facilities for working with IO
  objects

%prep
%setup -q -n %{pkgname}-%{version}

%build
# write .gemspec
%__gem_helper spec
cd ext/%{pkgname}
%{__ruby} extconf.rb
%{__make} \
	CC="%{__cc}" \
	LDFLAGS="%{rpmldflags}" \
	CFLAGS="%{rpmcflags} -fPIC"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_vendorlibdir},%{ruby_vendorarchdir},%{ruby_specdir}}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}
install -p ext/%{pkgname}/nio4r_ext.so $RPM_BUILD_ROOT%{ruby_vendorarchdir}
cp -p %{pkgname}-%{version}.gemspec $RPM_BUILD_ROOT%{ruby_specdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md CHANGES.md LICENSE.txt
%{ruby_vendorlibdir}/nio.rb
%{ruby_vendorlibdir}/nio
%attr(755,root,root) %{ruby_vendorarchdir}/nio4r_ext.so
%{ruby_specdir}/%{pkgname}-%{version}.gemspec

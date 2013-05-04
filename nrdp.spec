%define name nrdp-server
%define srcname nrdp
%define version 1.2
%define unmangled_version 1.2
%define release 1

Summary: Provide NRDP receiver for a Nagios server
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://assets.nagios.com/downloads/%{srcname}/%{srcname}.zip
Patch0: nrdp-default-location.patch
License: Nagios Open Software License
Group: Applications/System
BuildArch: noarch
Vendor: Nagios Enterprises, LLC
Packager: Colin Panisset <nonspecialist@clabber.com>
Url: http://www.nagios.org/download/addons
Requires: httpd php nagios

%description
NRDP is a flexible data transport mechanism and processor for Nagios. It is designed with a simple and powerful architecture that allows for it to be easily extended and customized to fit individual users' needs. It uses standard ports protocols (HTTP(S) and XML) and can be implemented as a replacement for NSCA.

%prep
%setup -q -n %{srcname}
%patch0

%build
/bin/true

%install
mkdir -p $RPM_BUILD_ROOT/var/www/nrdp $RPM_BUILD_ROOT/etc/httpd/conf.d
cp -r INSTALL.TXT LICENSE.TXT CHANGES.TXT server $RPM_BUILD_ROOT/var/www/nrdp
cp nrdp.conf $RPM_BUILD_ROOT/etc/httpd/conf.d

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%attr(0644, root, root) %config /etc/httpd/conf.d/nrdp.conf
%attr(-, nagios, nagios) /var/www/nrdp

%changelog
* Sat May 4 2013 Colin Panisset <nonspecialist@clabber.com> 1.2-1
- Initial creation of specfile
- separation of nrdp-server and nrdp-client into different packages due
  to different licenses

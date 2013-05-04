%define name nrdp
%define srcname nrdp
%define version 1.2
%define unmangled_version 1.2
%define release 1

Summary: NRDP capabilities for Nagios
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://assets.nagios.com/downloads/%{srcname}/%{srcname}.zip
Patch0: nrdp-default-location.patch
Patch1: nrdp-config-locations.patch
License: Nagios Open Software License
Group: Applications/System
BuildArch: noarch
Vendor: Nagios Enterprises, LLC
Packager: Colin Panisset <nonspecialist@clabber.com>
Url: http://www.nagios.org/download/addons

%description
NRDP is a flexible data transport mechanism and processor for Nagios. It is designed with a simple and powerful architecture that allows for it to be easily extended and customized to fit individual users' needs. It uses standard ports protocols (HTTP(S) and XML) and can be implemented as a replacement for NSCA.

%package server
Summary: PHP-based NRDP receiver for Nagios
Requires: httpd php nagios
%description server
The NRDP server provides a PHP receiver for NRDP events; it feeds received commands and events into the local Nagios external command file for processing by the Nagios daemon.

%package php-client
Summary: Simple PHP command-line NRDP sender for Nagios
Requires: php
%description php-client
A PHP implementation of an NRDP event sender for Nagios for submitting a single check result to an NRDP server.

%prep
%setup -q -n %{srcname}
%patch0
%patch1

%build
/bin/true

%install
mkdir -p $RPM_BUILD_ROOT/var/www/nrdp \
	 $RPM_BUILD_ROOT/etc/httpd/conf.d \
	 $RPM_BUILD_ROOT/usr/bin \
	 $RPM_BUILD_ROOT/var/spool/nagios/nrdp
cp -r INSTALL.TXT LICENSE.TXT CHANGES.TXT server \
	$RPM_BUILD_ROOT/var/www/nrdp
cp nrdp.conf $RPM_BUILD_ROOT/etc/httpd/conf.d
# necessary because it was written on Windows so line endings are screwed
# AND because, as required for most PHP installations, it doesn't have
# the '<?php' syntax as the lead-in
col -b < clients/send_nrdp.php | sed -e 's/^<?$/<?php/' \
	> $RPM_BUILD_ROOT/usr/bin/send_nrdp.php

%clean
rm -rf $RPM_BUILD_ROOT

%post php-client
/usr/sbin/alternatives --install /usr/bin/send_nrdp send_nrdp.php /usr/bin/send_nrdp.php 50

%postun php-client
/usr/sbin/alternatives --remove send_nrdp.php /usr/bin/send_nrdp.php

%files server
%defattr(-,root,root)
%attr(0644, root, root) %config /etc/httpd/conf.d/nrdp.conf
%attr(-, nagios, nagios) /var/www/nrdp
%attr(0770, nagios, nagios) /var/spool/nagios/nrdp

%files php-client
%defattr(-,root,root)
%attr(0755, root, root) /usr/bin/send_nrdp.php

%changelog
* Sat May 4 2013 Colin Panisset <nonspecialist@clabber.com> 1.2-1
- Initial creation of specfile
- separation of nrdp-server and nrdp-client into different packages
- adjust stock nrdp default config perms and paths to be more RHEL-like
- make use of alternatives to permit other non-php send_nrdp implementations
  to co-exist
- fix some windows-isms in send_nrdp

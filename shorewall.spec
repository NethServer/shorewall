Name: shorewall
Version: 1.4.8
Release: 2
Summary: Iptables-based firewall for Linux systems

Group: Applications/System
License: GPL
URL: http://www.shorewall.net/
Source: http://www.shorewall.net/pub/shorewall/shorewall-1.4.8/shorewall-1.4.8.tgz
Source1: shorewall.init
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires: iptables iproute

%description

The Shoreline Firewall, more commonly known as "Shorewall", is a Netfilter
(iptables) based firewall that can be used on a dedicated firewall system,
a multi-function gateway/router/server or on a standalone GNU/Linux system.

%package doc
Summary: Documentation for the Shoreline Firewall (Shorewall)
Group: Documentation

%description doc

This package contains the extensive and excellent documentation for the
Shoreline Firewall (aka Shorewall). This documentation can also be found at
http://www.shorewall.net/

%prep

%setup -q

# Clean backup doc files
rm -rf documentation/*~

%build

%install
rm -rf $RPM_BUILD_ROOT
export PREFIX=$RPM_BUILD_ROOT ; \
export OWNER=`id -n -u` ; \
export GROUP=`id -n -g` ;\
./install.sh %{_initrddir}
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT/%{_initrddir}/shorewall
# Create %ghost files
install -d $RPM_BUILD_ROOT/%{_localstatedir}/lib/shorewall
touch $RPM_BUILD_ROOT/%{_localstatedir}/lib/shorewall/{chains,nat,proxyarp,restarted,zones}

%clean
rm -rf $RPM_BUILD_ROOT

%post

if [ $1 -eq 1 ]; then
	echo \
"########################################################################
#      REMOVE THIS FILE AFTER YOU HAVE CONFIGURED SHOREWALL            #
########################################################################" \
	> %{_sysconfdir}/shorewall/startup_disabled
	/sbin/chkconfig --add shorewall;
fi

%preun

if [ $1 -eq 0 ]; then
	/sbin/chkconfig --del shorewall
	rm -f %{_sysconfdir}/shorewall/startup_disabled
fi

%files
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{_initrddir}/shorewall
%attr(0700,root,root) %dir %{_sysconfdir}/shorewall
%attr(0700,root,root) %dir %{_prefix}/share/shorewall
%attr(0700,root,root) %dir %{_localstatedir}/lib/shorewall
%attr(-,root,root) %ghost %{_localstatedir}/lib/shorewall/*
%attr(0600,root,root) %config %{_sysconfdir}/shorewall/*
%attr(0554,root,root) /sbin/shorewall
%attr(0600,root,root) %{_datadir}/shorewall/version
%attr(0444,root,root) %{_datadir}/shorewall/functions
%attr(0544,root,root) %{_datadir}/shorewall/firewall
%attr(0544,root,root) %{_datadir}/shorewall/help
%doc COPYING INSTALL changelog.txt releasenotes.txt tunnel

%files doc
%defattr(0644,root,root,0755)
%doc documentation/*

%changelog
* Tue Nov 11 2003 Miguel Armas <kuko@maarmas.com> - 1.4.8-1.fdr.2
- Clean backup doc files
- Fix some entries in files section

* Mon Nov 10 2003 Miguel Armas <kuko@maarmas.com> - 1.4.8-1.fdr.1
- Upgraded to shorewall 1.4.8

* Fri Oct 31 2003 Miguel Armas <kuko@maarmas.com> - 1.4.7-1.fdr.3.a
- Start shorewall *before* network for better security.
- Added clear command to shorewall init script to run "shorewall clear"
- Changed status command in shorewall init script to run "shorewall status"

* Thu Oct 30 2003 Miguel Armas <kuko@maarmas.com> - 1.4.7-1.fdr.2.a
- Lots of bugfixes in spec file (Thanks to Michael Schwendt)

* Sat Oct 25 2003 Miguel Armas <kuko@maarmas.com> - 1.4.7-1.fdr.1.a
- Fedorized package
- Split documentation in a subpackage (we don't need de docs in a production
firewall)

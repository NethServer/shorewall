Name: shorewall
Version: 2.4.5
Release: 1

Summary: Iptables-based firewall for Linux systems

Group: Applications/System
License: GPL
URL: http://www.shorewall.net/
Source: http://www.shorewall.net/pub/shorewall/2.4/shorewall-2.4.5/shorewall-2.4.5.tar.bz2
Patch0: shorewall-2.4.4-init.patch
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires: iptables iproute
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service

%description

The Shoreline Firewall, more commonly known as "Shorewall", is a Netfilter
(iptables) based firewall that can be used on a dedicated firewall system,
a multi-function gateway/router/server or on a standalone GNU/Linux system.

%prep

%setup -q
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
export PREFIX=$RPM_BUILD_ROOT ;\
export DEST=%{_initrddir} ;\

./install.sh
# Create %ghost files
install -d $RPM_BUILD_ROOT/%{_localstatedir}/lib/shorewall
touch $RPM_BUILD_ROOT/%{_localstatedir}/lib/shorewall/{chains,nat,proxyarp,restarted,zones,restore-base,restore-tail}

%clean
rm -rf $RPM_BUILD_ROOT

%post

if [ $1 = 1 ]; then
	/sbin/chkconfig --add shorewall;
fi

%preun

if [ $1 = 0 ]; then
	/sbin/service shorewall stop >/dev/null 2>&1
	/sbin/chkconfig --del shorewall
fi

%files
%defattr(0644,root,root,0755)

%attr(0755,root,root) %{_initrddir}/shorewall
%attr(0700,root,root) %dir %{_sysconfdir}/shorewall
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/shorewall/*
%attr(0755,root,root) %dir %{_datadir}/shorewall

%{_datadir}/shorewall/action.*
%{_datadir}/shorewall/actions.std
%{_datadir}/shorewall/bogons
%{_datadir}/shorewall/configpath
%{_datadir}/shorewall/rfc1918
%{_datadir}/shorewall/version

%attr(0754,root,root) %{_datadir}/shorewall/firewall
%attr(0754,root,root) %{_datadir}/shorewall/functions
%attr(0754,root,root) %{_datadir}/shorewall/help

%attr(0700,root,root) %dir %{_localstatedir}/lib/shorewall
%attr(0600,root,root) %ghost %{_localstatedir}/lib/shorewall/*
%attr(0750,root,root) /sbin/shorewall
%doc COPYING INSTALL changelog.txt releasenotes.txt tunnel

%changelog
* Sat Oct 08 2005 Robert Marcano <robert@marcanoonline.com> - 2.4.5-1
- Update to upstream version 2.4.5

* Wed Sep 28 2005 Robert Marcano <robert@marcanoonline.com> - 2.4.4-4
- Spec cleanup following review recomendations

* Tue Sep 27 2005 Robert Marcano <robert@marcanoonline.com>
- Update to 2.4.4, removing doc subpackage because it is not distributed
  with the source package anymore, it is on a different tarball

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

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

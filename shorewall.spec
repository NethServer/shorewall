Name: shorewall
Version: 3.4.4
Release: 1%{?dist}

Summary: Iptables-based firewall for Linux systems

Group: Applications/System
License: GPL
URL: http://www.shorewall.net/
Source: http://www.shorewall.net/pub/shorewall/3.4/shorewall-%{version}/shorewall-%{version}.tar.bz2
Patch0: shorewall-3.0.3-init.patch
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
touch $RPM_BUILD_ROOT/%{_localstatedir}/lib/shorewall/{chains,nat,proxyarp,restarted,zones,restore-base,restore-tail,state}

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
%{_datadir}/shorewall/configpath
%{_datadir}/shorewall/macro.*
%{_datadir}/shorewall/rfc1918
%{_datadir}/shorewall/version
%{_datadir}/shorewall/prog.*
%{_datadir}/shorewall/modules
%{_datadir}/shorewall/configfiles
%{_datadir}/shorewall/lib.*
%{_datadir}/shorewall/wait4ifup

%{_mandir}/man5/*
%{_mandir}/man8/*

%attr(0754,root,root) %{_datadir}/shorewall/firewall
%attr(0754,root,root) %{_datadir}/shorewall/functions
%attr(0754,root,root) %{_datadir}/shorewall/compiler

%attr(0700,root,root) %dir %{_localstatedir}/lib/shorewall
%attr(0600,root,root) %ghost %{_localstatedir}/lib/shorewall/*
%attr(0750,root,root) /sbin/shorewall
%doc COPYING INSTALL changelog.txt releasenotes.txt README.txt Samples

%changelog
* Mon Jun 18 2007 Robert Marcano <robert@marcanoonline.com> - 3.4.4-1
- Update to upstream 3.4.4

* Fri May 11 2007 Robert Marcano <robert@marcanoonline.com> - 3.4.3-1
- Update to upstream 3.4.3

* Sun Apr 15 2007 Robert Marcano <robert@marcanoonline.com> - 3.4.2-1
- Update to upstream 3.4.2

* Mon Mar 26 2007 Robert Marcano <robert@marcanoonline.com> - 3.4.1-1
- Update to upstream 3.4.1

* Tue Feb 06 2007 Robert Marcano <robert@marcanoonline.com> - 3.2.8-1
- Update to upstream 3.2.8

* Thu Dec 21 2006 Robert Marcano <robert@marcanoonline.com> - 3.2.7-1
- Update to upstream 3.2.7

* Tue Nov 07 2006 Robert Marcano <robert@marcanoonline.com> - 3.2.5-1
- Update to upstream 3.2.5

* Fri Sep 29 2006 Robert Marcano <robert@marcanoonline.com> - 3.2.4-1
- Update to upstream 3.2.4

* Mon Aug 28 2006 Robert Marcano <robert@marcanoonline.com> - 3.2.3-2
- Rebuild

* Sat Aug 26 2006 Robert Marcano <robert@marcanoonline.com> - 3.2.3-1
- Update to upstream 3.2.3

* Sun Aug 20 2006 Robert Marcano <robert@marcanoonline.com> - 3.2.2-1
- Update to upstream 3.2.2

* Fri Jul 28 2006 Robert Marcano <robert@marcanoonline.com> - 3.2.1-1
- Update to upstream 3.2.1

* Sat Jun 24 2006 Robert Marcano <robert@marcanoonline.com> - 3.2.0-0.1.RC4
- Update to upstream 3.2.0-RC4

* Thu Jun 01 2006 Robert Marcano <robert@marcanoonline.com> - 3.2.0-0.1.Beta8
- Update to upstream 3.2.0-Beta8

* Sun May 14 2006 Robert Marcano <robert@marcanoonline.com> - 3.2.0-0.1.Beta7
- Update to upstream 3.2.0-Beta7

* Fri Apr 14 2006 Robert Marcano <robert@marcanoonline.com> - 3.2.0-0.1.Beta4
- Update to upstream 3.2.0-Beta4

* Fri Mar 31 2006 Robert Marcano <robert@marcanoonline.com> - 3.0.6-1
- Update to upstream 3.0.6

* Mon Feb 13 2006 Robert Marcano <robert@marcanoonline.com> - 3.0.5-1
- Rebuild for Fedora Extras 5, Update to upstream 3.0.5

* Thu Jan 12 2006 Robert Marcano <robert@marcanoonline.com> - 3.0.4-1
- Update to upstream 3.0.4

* Tue Jan 03 2006 Robert Marcano <robert@marcanoonline.com> - 3.0.3-1
- Update to upstream 3.0.3

* Sun Nov 27 2005 Robert Marcano <robert@marcanoonline.com> - 3.0.2-1
- Update to upstream 3.0.2

* Fri Nov 11 2005 Robert Marcano <robert@marcanoonline.com> - 3.0.0-1
- Update to final 3.0.0 release

* Thu Nov 03 2005 Robert Marcano <robert@marcanoonline.com> - 3.0.0-0.3.RC3
- Update to upstream 3.0.0-RC3. Samples added to the doc directory

* Sun Oct 23 2005 Robert Marcano <robert@marcanoonline.com> - 3.0.0-0.3.RC2
- Update to upstream 3.0.0-RC2

* Thu Oct 17 2005 Robert Marcano <robert@marcanoonline.com> - 3.0.0-0.2.RC1
- Update to upstream 3.0.0-RC1

* Thu Oct 14 2005 Robert Marcano <robert@marcanoonline.com> - 3.0.0-0.1.Beta1
- Update to upstream 3.0.0-Beta1, package README.txt as a documentation file

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

Name:		oniguruma
Version:	6.8.2
Release:	2.1%{?dist}
Summary:	Regular expressions library

Group:		System Environment/Libraries
License:	BSD
URL:		https://github.com/kkos/oniguruma/
Source0:	https://github.com/kkos/oniguruma/releases/download/v%{version}/onig-%{version}.tar.gz
# Backport https://src.fedoraproject.org/rpms/oniguruma/blob/f29/f/0100-Apply-CVE-2019-13325-fix-to-6.9.1.patch
# (upstream: https://github.com/kkos/oniguruma/commit/c509265c5f6ae7264f7b8a8aae1cfa5fc59d108c)
Patch100:	oniguruma-6.8.2-CVE-2019-13225-fix.patch
Patch101:	oniguruma-6.8.2-CVE-2019-13224-fix.patch
Patch102:	oniguruma-6.8.2-CVE-2019-16163-fix.patch
Patch103:	oniguruma-6.8.2-CVE-2019-19012-fix.patch
Patch104:	oniguruma-6.8.2-CVE-2019-19203-fix.patch
Patch105:	oniguruma-6.8.2-CVE-2019-19204-fix.patch

%description
Oniguruma is a regular expressions library.
The characteristics of this library is that different character encoding
for every regular expression object can be specified.
(supported APIs: GNU regex, POSIX and Oniguruma native)


%package	devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name}%{?isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n onig-%{version}
%{__sed} -i.multilib -e 's|-L@libdir@||' onig-config.in

%if 0
for f in \
	README.ja \
	doc/API.ja \
	doc/FAQ.ja \
	doc/RE.ja
	do
	iconv -f EUC-JP -t UTF-8 $f > $f.tmp && \
		( touch -r $f $f.tmp ; %{__mv} -f $f.tmp $f ) || \
		%{__rm} -f $f.tmp
done
%endif

%patch100 -p1 -b .CVE-2019-13225
%patch101 -p1 -b .CVE-2019-13224
%patch102 -p1 -b .CVE-2019-16163
%patch103 -p1 -b .CVE-2019-19012
%patch104 -p1 -b .CVE-2019-19203
%patch105 -p1 -b .CVE-2019-19204

%build
%configure \
    --disable-silent-rules \
	--disable-static \
	--with-rubydir=%{_bindir}
%{__make} %{?_smp_mflags}


%install
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	INSTALL="%{__install} -c -p"
find $RPM_BUILD_ROOT -name '*.la' \
	-exec %{__rm} -f {} ';'

%check
%{__make} check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc	AUTHORS
%license	COPYING
%doc	HISTORY
%doc	README.md
%doc	index.html
%lang(ja)	%doc	README_japanese
%lang(ja)	%doc	index_ja.html

%{_libdir}/libonig.so.5*

%files devel
%defattr(-,root,root,-)
%doc	doc/API
%doc	doc/CALLOUTS.API
%doc	doc/CALLOUTS.BUILTIN
%doc	doc/FAQ
%doc	doc/RE
%lang(ja)	%doc	doc/API.ja
%lang(ja)	%doc	doc/CALLOUTS.API.ja
%lang(ja)	%doc	doc/CALLOUTS.BUILTIN.ja
%lang(ja)	%doc	doc/FAQ.ja
%lang(ja)	%doc	doc/RE.ja

%{_bindir}/onig-config

%{_libdir}/libonig.so
%{_includedir}/onig*.h
%{_libdir}/pkgconfig/%{name}.pc	

%changelog
* Fri Jan 05 2024 Vitezslav Crhonek <vcrhonek@redhat.com> - 6.8.2-2.1
- Fix CVE-2019-13224
  Resolves: RHEL-20648
- Fix CVE-2019-16163
  Resolves: RHEL-20642
- Fix CVE-2019-19012
  Resolves: RHEL-20636
- Fix CVE-2019-19203
  Resolves: RHEL-20630
- Fix CVE-2019-19204
  Resolves: RHEL-20624

* Fri Jun 26 2020 Jiri Kucera <jkucera@redhat.com> - 6.8.2-2
- Fix CVE-2019-13225
  Resolves: #1771052

* Mon Apr 23 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.8.2-1
- 6.8.2

* Sun Apr  1 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.8.1-1
- 6.8.1

* Fri Feb  9 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.7.1-1
- 6.7.1

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Dec 31 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.7.0-1
- 6.7.0

* Tue Sep  5 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.6.1-1
- 6.6.1

* Sun Aug 13 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.5.0-1
- 6.5.0

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul  5 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.4.0-1
- 6.4.0

* Tue May 30 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.3.0-1
- 6.3.0
  - CVEs 2017-9226 CVE-2017-9225 CVE-2017-9224 CVE-2017-9227 CVE-2017-9229 CVE-2017-9228

* Wed Apr 26 2017 Nils Philippsen <nils@redhat.com> - 6.2.0-2
- remove unnecessary BR: ruby

* Fri Apr 21 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.2.0-1
- 6.2.0

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Dec 28 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.1.3-1
- 6.1.3

* Fri Nov 11 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.1.2-1
- 6.1.2

* Sun Oct 30 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.1.1-1
- 6.1.1

* Mon Jul 11 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 6.0.0-1
- 6.0.0

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.9.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jan  2 2015 <mtasaka@fedoraproject.org> - 5.9.6-1
- 5.9.6

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Nov 11 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.9.5-1
- 5.9.5

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Apr 29 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.9.4-1
- 5.9.4

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan  4 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.9.3-1
- 5.9.3

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan  5 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 5.9.2-3
- F-17: rebuild against gcc47

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 15 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 5.9.2-1
- 5.9.2

* Sat Jul 25 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 5.9.1-3
- F-12: Mass rebuild

* Tue Feb 24 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 5.9.1-2
- F-11: Mass rebuild

* Sat Feb  9 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- Rebuild against gcc43

* Thu Dec 27 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 5.9.1-1
- 5.9.1

* Wed Dec  5 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 5.9.0-1
- Initial packaging


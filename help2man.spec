# Supported build option:
#
# --with nls ... build this package with --enable-nls 

Name:           help2man
Summary:        Create simple man pages from --help output
Version:        1.36.4
Release:        6%{?dist}
Group:          Development/Tools
License:        GPLv2+
URL:            http://www.gnu.org/software/help2man
Source:         ftp://ftp.gnu.org/gnu/help2man/help2man-%{version}.tar.gz

# Work around to https://bugzilla.redhat.com/show_bug.cgi?id=494089
Patch0:         help2man-1.36.4.diff
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%{!?_with_nls:BuildArch: noarch}
%{?_with_nls:BuildRequires: perl(Locale::gettext)}
%{?_with_nls:Requires: perl(Locale::gettext)}

Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description
help2man is a script to create simple man pages from the --help and
--version output of programs.

Since most GNU documentation is now in info format, this provides a
way to generate a placeholder man page pointing to that resource while
still providing some useful information.

%prep
%setup -q -n help2man-%{version}
%patch0 -p1
iconv -f ISO-8859-1 -t utf-8 THANKS > THANKS~
mv THANKS~ THANKS

%build

%configure %{!?_with_nls:--disable-nls}
make %{?_smp_mflags}

# Fix up manpage encoding
for f in help2man.*.h2m; do
  b=$(basename $f .h2m);
  c=$(grep 'charset: ISO-*' $f | sed -e 's,^.*: ,,')
  iconv -f $c -t utf-8 -o $b.1~ $b.1
  mv $b.1~ $b.1
done

%install
rm -fr $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
make install_l10n DESTDIR=$RPM_BUILD_ROOT

%clean
rm -fr $RPM_BUILD_ROOT

%post
/sbin/install-info %{_infodir}/help2man.info %{_infodir}/dir 2>/dev/null || :

%preun
if [ $1 -eq 0 ]; then
  /sbin/install-info --delete %{_infodir}/help2man.info \
    %{_infodir}/dir 2>/dev/null || :
fi

%files
%defattr(-, root, root,-)
%doc README NEWS THANKS COPYING
%{_bindir}/help2man
%{_infodir}/*
%{_mandir}/man1/*

%if "%{?_with_nls}"
%{_libdir}/*.so
%endif
%lang(pl) %{_datadir}/locale/pl/LC_MESSAGES/help2man.mo
%lang(fi) %{_datadir}/locale/fi/LC_MESSAGES/help2man.mo
%lang(fr) %{_datadir}/locale/fr/LC_MESSAGES/help2man.mo
%lang(sv) %{_datadir}/locale/sv/LC_MESSAGES/help2man.mo
%lang(pl) %{_mandir}/pl/man1/*
%lang(fi) %{_mandir}/fi/man1/*
%lang(fr) %{_mandir}/fr/man1/*
%lang(sv) %{_mandir}/sv/man1/*

%changelog
* Tue Feb 23 2010 Ondrej Vasik <ovasik@redhat.com> - 1.36.4-6
- do ship COPYING file in %%doc

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 1.36.4-5.1
- Rebuilt for RHEL 6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.36.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon May 18 2009 corsepiu@fedoraproject.org> - 1.36.4-4
- Apply patch from http://bugs.gentoo.org/show_bug.cgi?id=237378#c6
  to address BZ #494089.

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.36.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb 10 2008 Ralf Corsépius <rc040203@freenet.de> - 1.36.4-2
- Update license tag.
- Convert THANKS to utf-8.

* Tue Sep 05 2006 Ralf Corsépius <rc040203@freenet.de> - 1.36.4-1
- Upstream update.
- utf-8 encode l10n'd man pages.

* Fri Dec 23 2005 Ralf Corsépius <rc04203@freenet.de> - 1.36.3-1
- Upstream update.
- Add build option --with nls.

* Fri Dec 23 2005 Ralf Corsépius <rc04203@freenet.de> - 1.35.1-2
- Fix disttag (#176473).
- Cleanup spec.

* Fri Apr 29 2005 Ralf Corsepius <ralf[AT]links2linux.de> - 1.35.1-1
- Update to 1.35.1
- Minor spec fixes.

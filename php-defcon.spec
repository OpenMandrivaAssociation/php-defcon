%define modname defcon
%define dirname %{modname}
%define soname %{modname}.so
%define inifile B18_%{modname}.ini

Summary:	PHP Defcon extension
Name:		php-%{modname}
Version:	1.0.0
Release:	6
Group:		Development/PHP
License:	PHP
URL:		https://www.xarg.org/project/php-defcon/
Source0:	http://www.xarg.org/download/defcon-%{version}.tar.gz
Source1:	B18_defcon.ini
Source2:	defcon.conf
Patch0:		defcon-1.0.0-php54x.diff
BuildRequires:	php-devel >= 3:5.2.0
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
PHP Defcon is an Extension for PHP to define constants that are available
during the whole server runtime - from server start to shutdown.

%prep

%setup -q -n %{modname}-%{version}

%patch0 -p0

cp %{SOURCE1} %{inifile}
cp %{SOURCE2} defcon.conf

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" config.m4

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}
%make
mv modules/*.so .

%install
rm -rf %{buildroot} 

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m0755 %{soname} %{buildroot}%{_libdir}/php/extensions/
install -m0644 %{inifile} %{buildroot}%{_sysconfdir}/php.d/%{inifile}
install -m0644 defcon.conf %{buildroot}%{_sysconfdir}/

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc CREDIT
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/defcon.conf
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}



%changelog
* Sun May 06 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-5mdv2012.0
+ Revision: 797124
- fix build
- rebuild for php-5.4.x

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-4
+ Revision: 761215
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-3
+ Revision: 696408
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-2
+ Revision: 695381
- rebuilt for php-5.3.7

* Fri May 20 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-1
+ Revision: 676255
- import php-defcon


* Fri May 20 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-1mdv2010.2
- initial Mandriva package

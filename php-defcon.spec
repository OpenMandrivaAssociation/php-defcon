%define modname defcon
%define dirname %{modname}
%define soname %{modname}.so
%define inifile B18_%{modname}.ini

Summary:	PHP Defcon extension
Name:		php-%{modname}
Version:	1.0.0
Release:	%mkrel 5
Group:		Development/PHP
License:	PHP
URL:		http://www.xarg.org/project/php-defcon/
Source0:	http://www.xarg.org/download/defcon-%{version}.tar.gz
Source1:	B18_defcon.ini
Source2:	defcon.conf
BuildRequires:	php-devel >= 3:5.2.0
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
PHP Defcon is an Extension for PHP to define constants that are available
during the whole server runtime - from server start to shutdown.

%prep

%setup -q -n %{modname}-%{version}

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


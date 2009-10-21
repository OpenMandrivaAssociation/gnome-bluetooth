%define major	7
%define libname %mklibname %name %{major}
%define develname %mklibname -d %name

Name: 	 	gnome-bluetooth
Summary: 	GNOME Bluetooth Subsystem
Version: 	2.28.3
Release: %mkrel 1
Epoch: 1
Source:		http://ftp.gnome.org/pub/GNOME/sources/gnome-bluetooth/%{name}-%{version}.tar.bz2
#gw missing file: http://bugzilla.gnome.org/show_bug.cgi?id=589280
Source1: DBusGLib-1.0.gir
URL:		http://usefulinc.com/software/gnome-bluetooth/
#gw lib is LGPL, main app is GPL
License:	GPLv2+ and LGPLv2+
Group:		Graphical desktop/GNOME
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
BuildRequires:	gettext
BuildRequires:	libbtctl-devel >= 0.9
BuildRequires:	openobex-devel
BuildRequires:	unique-devel
BuildRequires:	libnotify-devel
BuildRequires:	libGConf2-devel
BuildRequires:	hal-devel
BuildRequires:	bluez-devel bluez-sdp-devel gob2 librsvg-devel
BuildRequires:  gobject-introspection-devel gir-repository
BuildRequires:  intltool
BuildRequires:  gnome-doc-utils
Requires(post)  : desktop-file-utils
Requires(postun): desktop-file-utils
Requires: gvfs-obexftp
Requires: bluez
Requires: obexd
Provides: bluez-pin
Provides: bluez-gnome
Obsoletes: bluez-gnome
Provides: bluez-gnome-analyzer
Obsoletes: bluez-gnome-analyzer



%description
The GNOME Bluetooth Subsystem contains a Bonobo server to control Bluetooth
devices, and a simple GUI to explore which devices are available
(gnome-bluetooth-admin).

%package -n %libname
Group:		System/Libraries
Summary: 	GNOME bluetooth library

%description -n %libname
Library from GNOME-Bluetooth.

%package -n %develname
Group:		Development/C
Summary:	Static libraries and header files from %name
Provides:	%name-devel = %version-%release
Provides:	libgnomebt-devel = %version-%release
Requires:	%libname = %{epoch}:%version
Requires:	libbtctl-devel >= 0.6
Provides: %mklibname -d %name 0
Obsoletes:  %mklibname -d %name 0
Provides: %mklibname -d %name 1
Obsoletes:  %mklibname -d %name 1


%description -n %develname
Static libraries and header files from %name

%prep
%setup -q
cp %SOURCE1 lib

%build
%configure2_5x --enable-shared --disable-static --disable-desktop-update \
	       --disable-schemas-install --disable-icon-update
make
										
%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std GIRDIR=%_datadir/gir-1.0 TYPELIBDIR=%_libdir/girepository-1.0

%find_lang %{name}2
%find_lang %{name} --with-gnome
for omf in %buildroot%_datadir/omf/*/*[_-]??.omf;do 
echo "%lang($(basename $omf|sed -e s/.*-// -e s/.omf//)) $(echo $omf|sed -e s!%buildroot!!)" >> %name.lang
done
cat %name.lang >> %{name}2.lang

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig
%endif

%define schemas bluetooth-manager
%if %mdvver < 200900
%post_install_gconf_schemas %schemas
%update_icon_cache hicolor
%update_desktop_database
%endif

%preun
%preun_uninstall_gconf_schemas %schemas

%if %mdvver < 200900
%clean_desktop_database
%clean_icon_cache hicolor
%endif


%files -f %{name}2.lang
%defattr(-,root,root)
%doc README AUTHORS
%_sysconfdir/gconf/schemas/bluetooth-manager.schemas
%_sysconfdir/xdg/autostart/bluetooth-applet.desktop
%_bindir/*
%_datadir/applications/bluetooth-properties.desktop
%{_datadir}/%name
%_mandir/man1/*
%_datadir/icons/hicolor/*/*/*.*
%dir %_datadir/omf/%name
%_datadir/omf/%name/%name-C.omf
%dir %_libdir/%name
%dir %_libdir/%name/plugins
%_libdir/%name/plugins/libgbtgeoclue.*

%files -n %libname
%defattr(-,root,root)
%{_libdir}/lib%name.so.%{major}*
%_libdir/girepository-1.0/GnomeBluetooth-1.0.typelib

%files -n %develname
%defattr(-,root,root)
%_datadir/gtk-doc/html/%name
%{_includedir}/%name
%attr(644,root,root)%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%_datadir/gir-1.0/GnomeBluetooth-1.0.gir

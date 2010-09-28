%define major	8
%define libname %mklibname %name %{major}
%define develname %mklibname -d %name

Name: 	 	gnome-bluetooth
Summary: 	GNOME Bluetooth Subsystem
Version: 	2.32.0
Release: %mkrel 1
Epoch: 1
Source:		http://ftp.gnome.org/pub/GNOME/sources/gnome-bluetooth/%{name}-%{version}.tar.bz2
URL:		http://usefulinc.com/software/gnome-bluetooth/
#gw lib is LGPL, main app is GPL
License:	GPLv2+ and LGPLv2+
Group:		Graphical desktop/GNOME
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
BuildRequires:	glib2-devel >= 2.25.7
BuildRequires:	gtk+2-devel
BuildRequires:	gettext
BuildRequires:	libbtctl-devel >= 0.9
BuildRequires:	openobex-devel
BuildRequires:	unique-devel
BuildRequires:	libnotify-devel
BuildRequires:	libGConf2-devel
BuildRequires:	hal-devel
BuildRequires:	bluez-devel bluez-sdp-devel gob2 librsvg-devel
BuildRequires:	nautilus-sendto-devel
BuildRequires:  gobject-introspection-devel
# for DBusGLib-1.0.gir
BuildRequires:	gir-repository >= 0.6.5-4 
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
The gnome-bluetooth package contains graphical utilities to setup,
monitor and use Bluetooth devices.

%package -n %libname
Group:		System/Libraries
Summary: 	GNOME bluetooth library
Conflicts:	%{_lib}gnome-bluetooth7 < 1:2.31

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

%package -n nautilus-sendto-bluetooth
Summary: Send files from nautilus to bluetooth
Group: Graphical desktop/GNOME
Requires: nautilus-sendto
Requires: %name

%description -n nautilus-sendto-bluetooth
This application provides integration between nautilus and bluetooth.
It adds a Nautilus context menu component ("Send To...") and features
a dialog for insert the bluetooth device which you want to send the
file/files.

%prep
%setup -q

%build
%configure2_5x --enable-shared --disable-static --disable-desktop-update \
	       --disable-icon-update
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

rm -f %buildroot%_libdir/nautilus-sendto/plugins/*.la

%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}2.lang
%defattr(-,root,root)
%doc README AUTHORS
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
%_datadir/GConf/gsettings/gnome-bluetooth
%_datadir/glib-2.0/schemas/org.gnome.Bluetooth.gschema.xml

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

%files -n nautilus-sendto-bluetooth
%defattr(-,root,root)
%_libdir/nautilus-sendto/plugins/libnstbluetooth.so
%_datadir/GConf/gsettings/gnome-bluetooth-nst
%_datadir/glib-2.0/schemas/org.gnome.Bluetooth.nst.gschema.xml

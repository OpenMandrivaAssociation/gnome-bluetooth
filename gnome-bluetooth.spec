%define major	10
%define major_applet	0
%define gir_major	1.0
%define libname		%mklibname %{name} %{major}
%define libapplet	%mklibname %{name}-applet %{major_applet}
%define girname		%mklibname %{name}-gir %{gir_major}
%define girapplet	%mklibname %{name}-applet-gir %{gir_major}
%define develname	%mklibname -d %{name}

Name: 	 	gnome-bluetooth
Summary: 	GNOME Bluetooth Subsystem
Epoch:		1
Version: 	3.4.0
Release:	0
#gw lib is LGPL, main app is GPL
License:	GPLv2+ and LGPLv2+
Group:		Graphical desktop/GNOME
URL:		http://usefulinc.com/software/gnome-bluetooth/
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-bluetooth/%{name}-%{version}.tar.xz

BuildRequires:  intltool
BuildRequires:	GConf2
BuildRequires:	gettext
BuildRequires:  gnome-doc-utils
BuildRequires:	gnome-common
BuildRequires:	gtk-doc
BuildRequires:	pkgconfig(glib-2.0) >= 2.25.7
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(unique-3.0)
BuildRequires:	pkgconfig(libnotify)
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gconf-2.0)
BuildRequires:	pkgconfig(nautilus-sendto)
BuildRequires:  pkgconfig(gobject-introspection-1.0)

Requires: gvfs-obexftp
Requires: bluez
Requires: obexd

%description
The gnome-bluetooth package contains graphical utilities to setup,
monitor and use Bluetooth devices.

%package -n %{libname}
Group:		System/Libraries
Summary: 	GNOME bluetooth library
Conflicts:	%{_lib}gnome-bluetooth7 < 1:2.31

%description -n %{libname}
Library from GNOME-Bluetooth.

%package -n %{libapplet}
Group:		System/Libraries
Summary: 	GNOME bluetooth Applet library

%description -n %{libapplet}
Library from GNOME-Bluetooth Applet

%package -n %{girname}
Group:		System/Libraries
Summary:	GObject Introspection interface for %{name}
Requires:	%{libname} = %{EVRD}

%description -n %{girname}
GObject Introspection interface for %{name}.

%package -n %{girapplet}
Group:		System/Libraries
Summary:	GObject Introspection interface for %{name} applet
Requires:	%{libapplet} = %{EVRD}

%description -n %{girapplet}
GObject Introspection interface for %{name} applet. 

%package -n %{develname}
Group:		Development/C
Summary:	Development libraries and header files from %{name}
Requires:	%{libname} = %{EVRD}
Requires:	%{libapplet} = %{EVRD}
Provides:	%{name}-devel = %{version}-%{release}


%description -n %{develname}
Development libraries and header files from %{name}

%package -n nautilus-sendto-bluetooth
Summary: Send files from nautilus to bluetooth
Group: Graphical desktop/GNOME
Requires: nautilus-sendto
Requires: %{name} = %{version}-%{release}

%description -n nautilus-sendto-bluetooth
This application provides integration between nautilus and bluetooth.
It adds a Nautilus context menu component ("Send To...") and features
a dialog for insert the bluetooth device which you want to send the
file/files.

%prep
%setup -q
%apply_patches

%build
%configure2_5x \
	--enable-shared \
	--disable-static \
	--disable-desktop-update \
	--disable-icon-update

%make
										
%install
rm -rf %{buildroot}
%makeinstall_std
find %buildroot -name *.la | xargs rm
%find_lang %{name}2 --all-name --with-gnome

#for omf in %{buildroot}%{_datadir}/omf/*/*[_-]??.omf;do 
#echo "%lang($(basename $omf|sed -e s/.*-// -e s/.omf//)) $(echo $omf|sed -e s!%{buildroot}!!)" >> %{name}.lang
#done
#cat %{name}.lang >> %{name}2.lang

# remove some quite annoying /usr/usr
perl -pi -e "s|/usr/usr/%{_lib}|%{_libdir}|g" %{buildroot}%{_libdir}/*.la

%files -f %{name}2.lang
%doc README AUTHORS
%{_sysconfdir}/xdg/autostart/bluetooth-applet.desktop
%{_bindir}/*
%{_datadir}/applications/bluetooth-sendto.desktop
%{_datadir}/applications/bluetooth-wizard.desktop
%{_datadir}/icons/hicolor/*/*/*.*
%{_datadir}/%{name}
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/plugins
%{_libdir}/%{name}/plugins/libgbtgeoclue.*
%{_libdir}/gnome-bluetooth/libgnome-bluetooth-applet.so
%{_mandir}/man1/*

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}*

%files -n %{libapplet}
%{_libdir}/gnome-bluetooth/libgnome-bluetooth-applet.so.%{major_applet}*

%files -n %{girname}
%{_libdir}/girepository-1.0/GnomeBluetooth-%{gir_major}.typelib

%files -n %{girapplet}
%{_libdir}/gnome-bluetooth/GnomeBluetoothApplet-%{gir_major}.typelib

%files -n %{develname}
%{_datadir}/gtk-doc/html/%{name}
%{_includedir}/%{name}
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gir-1.0/GnomeBluetooth-1.0.gir

%files -n nautilus-sendto-bluetooth
%{_libdir}/nautilus-sendto/plugins/libnstbluetooth.so
%{_datadir}/GConf/gsettings/gnome-bluetooth-nst
%{_datadir}/glib-2.0/schemas/org.gnome.Bluetooth.nst.gschema.xml

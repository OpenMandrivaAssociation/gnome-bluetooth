%define _disable_ld_no_undefined 1
%define url_ver %(echo %{version}|cut -d. -f1,2)

%define	major	11
%define	maj_app	0
%define	gir_maj	1.0
%define	libname	%mklibname %{name} %{major}
%define	libapp	%mklibname %{name}-applet %{maj_app}
%define	girname	%mklibname %{name}-gir %{gir_maj}
%define	girapp	%mklibname %{name}-applet-gir %{gir_maj}
%define	devname	%mklibname -d %{name}

Summary: 	GNOME Bluetooth Subsystem
Name: 	 	gnome-bluetooth
Epoch:		1
Version: 	3.6.1
Release:	4
License:	GPLv2+ and LGPLv2+
Group:		Graphical desktop/GNOME
Url:		http://usefulinc.com/software/gnome-bluetooth/
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-bluetooth/%{url_ver}/%{name}-%{version}.tar.xz
Source1:	61-gnome-bluetooth-rfkill.rules

BuildRequires:	intltool itstool
BuildRequires:	GConf2
BuildRequires:	gettext
BuildRequires:	gnome-common
BuildRequires:	gtk-doc
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gnome-doc-utils)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(unique-3.0)
BuildRequires:	pkgconfig(libnotify)
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gconf-2.0)
BuildRequires:	pkgconfig(nautilus-sendto)
BuildRequires:	pkgconfig(gobject-introspection-1.0)

Requires:	gvfs-obexftp
Requires:	bluez
Requires:	obexd

%description
The gnome-bluetooth package contains graphical utilities to setup,
monitor and use Bluetooth devices.

%package -n	%{libname}
Group:		System/Libraries
Summary: 	GNOME bluetooth library
Conflicts:	%{_lib}gnome-bluetooth7 < 1:2.31

%description -n	%{libname}
Library from GNOME-Bluetooth.

%package -n	%{libapp}
Group:		System/Libraries
Summary: 	GNOME bluetooth Applet library

%description -n %{libapp}
Library from GNOME-Bluetooth Applet

%package -n	%{girname}
Group:		System/Libraries
Summary:	GObject Introspection interface for %{name}

%description -n	%{girname}
GObject Introspection interface for %{name}.

%package -n	%{girapp}
Group:		System/Libraries
Summary:	GObject Introspection interface for %{name} applet

%description -n	%{girapp}
GObject Introspection interface for %{name} applet. 

%package -n	%{devname}
Group:		Development/C
Summary:	Development libraries and header files from %{name}
Requires:	%{libname} = %{EVRD}
Requires:	%{libapp} = %{EVRD}
Requires:	%{girname} = %{EVRD}
Requires:	%{girapp} = %{EVRD}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{devname}
Development libraries and header files from %{name}

%package -n	nautilus-sendto-bluetooth
Summary:	Send files from nautilus to bluetooth
Group:		Graphical desktop/GNOME
Requires:	nautilus-sendto
Requires:	%{name} = %{EVRD}

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
%makeinstall_std
%find_lang %{name}2 --all-name --with-gnome

mkdir -p %{buildroot}/lib/udev/rules.d
install -m644 %{SOURCE1} %{buildroot}/lib/udev/rules.d/

%files -f %{name}2.lang
%doc README AUTHORS
%{_sysconfdir}/xdg/autostart/bluetooth-applet.desktop
%{_bindir}/*
%{_datadir}/applications/bluetooth-sendto.desktop
%{_datadir}/applications/bluetooth-wizard.desktop
%{_datadir}/%{name}
%{_iconsdir}/hicolor/*/*/*.*
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/plugins
%{_libdir}/%{name}/plugins/libgbtgeoclue.*
%{_mandir}/man1/*
/lib/udev/rules.d/*

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}*

%files -n %{libapp}
%{_libdir}/gnome-bluetooth/libgnome-bluetooth-applet.so.%{maj_app}*

%files -n %{girname}
%{_libdir}/girepository-1.0/GnomeBluetooth-%{gir_maj}.typelib

%files -n %{girapp}
%{_libdir}/gnome-bluetooth/GnomeBluetoothApplet-%{gir_maj}.typelib

%files -n %{devname}
%{_datadir}/gtk-doc/html/%{name}
%{_includedir}/%{name}
%{_libdir}/*.so
%{_libdir}/gnome-bluetooth/libgnome-bluetooth-applet.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gir-1.0/GnomeBluetooth-1.0.gir

%files -n nautilus-sendto-bluetooth
%{_libdir}/nautilus-sendto/plugins/libnstbluetooth.so
%{_datadir}/GConf/gsettings/gnome-bluetooth-nst
%{_datadir}/glib-2.0/schemas/org.gnome.Bluetooth.nst.gschema.xml


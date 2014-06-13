%define major		11
%define major_applet	0
%define gi_major	1.0

%define libname		%mklibname %{name} %{major}
%define libnameapplet	%mklibname %{name}-applet %{major_applet}
%define develname	%mklibname -d %{name}
%define girname		%mklibname %{name}-gir %{gi_major}
%define girnameapplet	%mklibname %{name}-applet-gir %{gi_major}

%define url_ver	%(echo %{version}|cut -d. -f1,2)
%define _disable_ld_no_undefined 1

Name: 	 	gnome-bluetooth
Summary: 	GNOME Bluetooth Subsystem
Version: 	3.8.1
Release: 	6
Epoch:		1
Source0:	http://download.gnome.org/sources/%{name}/%{url_ver}/%{name}-%{version}.tar.xz
Source1:	61-gnome-bluetooth-rfkill.rules
URL:		http://usefulinc.com/software/gnome-bluetooth/
#gw lib is LGPL, main app is GPL
License:	GPLv2+ and LGPLv2+
Group:		Graphical desktop/GNOME
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(gio-unix-2.0)
BuildRequires:	pkgconfig(glib-2.0) >= 2.29.90
BuildRequires:	pkgconfig(gmodule-2.0)
BuildRequires:	pkgconfig(gmodule-export-2.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(libnotify) >= 0.7.0
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xi)
BuildRequires:	gnome-common
BuildRequires:	gobject-introspection-devel >= 0.9.5
BuildRequires:	intltool
BuildRequires:	itstool
BuildRequires:	libxml2-utils
Requires:	gvfs-obexftp
Requires:	bluez
Requires:	obexd
Requires:	pulseaudio-module-bluetooth
Provides:	bluez-pin

%description
The gnome-bluetooth package contains graphical utilities to setup,
monitor and use Bluetooth devices.

%package -n %{libname}
Group:		System/Libraries
Summary: 	GNOME bluetooth library
Conflicts:	%{_lib}gnome-bluetooth7 < 1:2.31

%description -n %{libname}
Library from GNOME-Bluetooth.

%package -n %{libnameapplet}
Group:		System/Libraries
Summary: 	GNOME bluetooth Applet library

%description -n %{libnameapplet}
Library from GNOME-Bluetooth Applet

%package -n %{girnameapplet}
Group:		System/Libraries
Summary:	GObject Introspection interface for %{name} applet
Requires:	%{libnameapplet} = %{epoch}:%{version}-%{release}

%description -n %{girnameapplet}
GObject Introspection interface for %{name} applet. 

%package -n %{girname}
Group:		System/Libraries
Summary:	GObject Introspection interface for %{name}
Requires:	%{libname} = %{epoch}:%{version}-%{release}

%description -n %{girname}
GObject Introspection interface for %{name}.

%package -n %{develname}
Group:		Development/C
Summary:	Development files and header files from %{name}
Provides:	lib%{name}-devel = %{epoch}:%{version}-%{release}
Provides:	%{name}-devel = %{epoch}:%{version}-%{release}
Provides:	libgnomebt-devel = %{epoch}:%{version}-%{release}
Requires:	%{libname} = %{epoch}:%{version}-%{release}
Requires:	%{libnameapplet} = %{epoch}:%{version}-%{release}

%description -n %{develname}
Development files and header files from %{name}.

%prep
%setup -q

%build
%configure2_5x \
	--enable-shared \
	--disable-static \
	--disable-desktop-update \
	--disable-icon-update \
	--disable-schemas-compile
%make

%install
%makeinstall_std

mkdir -p %{buildroot}%{_udevrulesdir}
install %{SOURCE1} %{buildroot}%{_udevrulesdir}/

%find_lang %{name}2 --all-name --with-gnome

# Remove .la files
find %{buildroot} -name "*.la" -exec rm -rf {} \;

%files -f %{name}2.lang
%doc README AUTHORS
%{_udevrulesdir}/61-gnome-bluetooth-rfkill.rules
%{_bindir}/*
%{_datadir}/applications/bluetooth-sendto.desktop
%{_datadir}/applications/bluetooth-wizard.desktop
%{_datadir}/%{name}
%{_mandir}/man1/*
%{_datadir}/icons/hicolor/*/*/*.*
%{_libdir}/%{name}/plugins/libgbtgeoclue.*

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}*

%files -n %{libnameapplet}
%{_libdir}/gnome-bluetooth/libgnome-bluetooth-applet.so.%{major_applet}*

%files -n %{girnameapplet}
%{_libdir}/gnome-bluetooth/GnomeBluetoothApplet-%{gi_major}.typelib

%files -n %{girname}
%{_libdir}/girepository-1.0/GnomeBluetooth-%{gi_major}.typelib

%files -n %{develname}
%doc %{_datadir}/gtk-doc/html/%{name}
%{_includedir}/%{name}
%{_libdir}/lib%{name}.so
%{_libdir}/gnome-bluetooth/libgnome-bluetooth-applet.so
%{_datadir}/gir-1.0/GnomeBluetooth-%{gi_major}.gir
%{_libdir}/pkgconfig/*.pc


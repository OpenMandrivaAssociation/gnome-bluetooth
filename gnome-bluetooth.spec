%define major		13
%define gi_major	3.0
%define	api		3

# Let's add compact package g-bluetooth with version 3.34.X (gtk3) to allow works other non gmome packages like blueberry/
# That's why we need add also new api to file name to avoid conflicting.

%define libname		%mklibname %{name} %{api} %{major}
%define develname	%mklibname -d %{name} %{api}
%define girname		%mklibname %{name}-gir %{api} %{gi_major}

%define url_ver	%(echo %{version}|cut -d. -f1,2)
%define _disable_ld_no_undefined 1
%define _disable_rebuild_configure 1

Name: 	 	gnome-bluetooth
Summary: 	GNOME Bluetooth Subsystem
Version:	42.0
Release:	1
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
BuildRequires:	pkgconfig(gsound)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(gtk4)
BuildRequires:	pkgconfig(libnotify) >= 0.7.0
BuildRequires:	pkgconfig(libudev)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(libadwaita-1)
BuildRequires:	pkgconfig(libcanberra-gtk3)
BuildRequires:	pkgconfig(upower-glib)
BuildRequires:	python3dist(python-dbusmock)
BuildRequires:	gnome-common
BuildRequires:	gobject-introspection-devel >= 0.9.5
BuildRequires:	intltool
BuildRequires:	itstool
BuildRequires:	libxml2-utils
BuildRequires:  meson
BuildRequires:  gtk-doc
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

%description -n %{develname}
Development files and header files from %{name}.

%prep
%setup -q

%build
%meson          \
	-Dgtk_doc=true
	
%meson_build

%install
%meson_install

mkdir -p %{buildroot}%{_udevrulesdir}
install %{SOURCE1} %{buildroot}%{_udevrulesdir}/

%find_lang %{name}-%{gi_major} --all-name --with-gnome

# Remove .la files
find %{buildroot} -name "*.la" -exec rm -rf {} \;

%files -f %{name}-%{gi_major}.lang
%doc README.md AUTHORS
%{_udevrulesdir}/61-gnome-bluetooth-rfkill.rules
%{_bindir}/*
%{_datadir}/applications/bluetooth-sendto.desktop
%{_mandir}/man1/*
%{_datadir}/gnome-bluetooth-%{gi_major}/
#{_datadir}/icons/hicolor/*/*/*.*

%files -n %{libname}
%{_libdir}/lib%{name}-%{gi_major}.so.%{major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/GnomeBluetooth-%{gi_major}.typelib

%files -n %{develname}
#doc %{_datadir}/gtk-doc/html/%{name}
%{_includedir}/%{name}
%{_libdir}/lib%{name}-%{gi_major}.so
%{_libdir}/libgnome-bluetooth-ui-%{gi_major}.so
%{_libdir}/pkgconfig/gnome-bluetooth-%{gi_major}.pc
%{_libdir}/pkgconfig/gnome-bluetooth-ui-%{gi_major}.pc
%{_datadir}/gir-1.0/GnomeBluetooth-%{gi_major}.gir


%define major	1
%define libname %mklibname gnomebt %{major}
%define develname %mklibname -d gnomebt

Name: 	 	gnome-bluetooth
Summary: 	GNOME Bluetooth Subsystem
Version: 	0.12.0
Release: %mkrel 2

Source:		http://ftp.gnome.org/pub/GNOME/sources/gnome-bluetooth/%{name}-%{version}.tar.bz2
URL:		http://usefulinc.com/software/gnome-bluetooth/
#gw lib is LGPL, main app is GPL
License:	GPLv2+ and LGPLv2+
Group:		Graphical desktop/GNOME
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
BuildRequires:	gettext
BuildRequires:	libbtctl-devel >= 0.9
BuildRequires:	openobex-devel
BuildRequires:	libglade2.0-devel libgnomeui2-devel libGConf2-devel
BuildRequires:	bluez-devel bluez-sdp-devel gob2 librsvg-devel
BuildRequires:  intltool
BuildRequires:  pygtk2.0-devel python-gobject-devel
Requires:	pygtk2.0-libglade
Requires:	gnome-python gnome-python-gnomevfs python-libbtctl
Provides:	gnome-obex-server

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
Requires:	%libname = %version
Requires:	libbtctl-devel >= 0.6
Provides: %mklibname -d %name 0
Obsoletes:  %mklibname -d %name 0
Provides: %mklibname -d %name 1
Obsoletes:  %mklibname -d %name 1


%description -n %develname
Static libraries and header files from %name

%prep
%setup -q

%build
%configure2_5x --enable-shared --enable-static
%make
										
%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std
mv $RPM_BUILD_ROOT%_datadir/pixmaps/* $RPM_BUILD_ROOT%_datadir/%name/pixmaps/


%find_lang %name

%if %_lib != lib
mv %buildroot%_prefix/lib/python* %buildroot%_libdir
%endif

rm -f %buildroot%py_platsitedir/gnomebt/*a

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files -f %{name}.lang
%defattr(-,root,root)
%doc README AUTHORS ChangeLog
%py_platsitedir/gnomebt
%{_datadir}/%name

%files -n %libname
%defattr(-,root,root)
%{_libdir}/libgnomebt.so.%{major}*

%files -n %develname
%defattr(-,root,root)
%{_includedir}/%name
%{_libdir}/*.a
%attr(644,root,root)%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc



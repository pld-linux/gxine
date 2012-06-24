#
# Conditional build:
%bcond_without	lirc	# without LIRC support
#
Summary:	GTK+ based GUI for xine-libraries
Summary(de):	GTK+ basierende grafische Oberfl�che f�r die xine-Bibliotheken
Summary(pl):	Oparty na GTK+ graficzny interfejs do bibliotek XINE
Name:		gxine
Version:	0.5.9
Release:	1
License:	GPL
Group:		X11/Applications/Multimedia
Source0:	http://dl.sourceforge.net/xine/%{name}-%{version}.tar.bz2
# Source0-md5:	e0c7bddeed0850fb5a3a874f4df1ffca
Patch0:		%{name}-desktop.patch
Patch1:		%{name}-plugindir.patch
URL:		http://xine.sourceforge.net/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.9
BuildRequires:	gtk+2-devel >= 1:2.6.0
BuildRequires:	js-devel
BuildRequires:	libtool
%{?with_lirc:BuildRequires:	lirc-devel}
BuildRequires:	nspr-devel
BuildRequires:	pango-devel >= 1.12
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.357
BuildRequires:	xine-lib-devel >= 2:1.0.1
BuildRequires:	xorg-lib-libXaw-devel
BuildRequires:	xorg-lib-libXinerama-devel
Requires:	xine-lib >= 2:1.0.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
xine is a fully-featured free audio/video player for unix-like systems
which uses libxine for audio/video decoding and playback. For more
informations on what formats are supported, please refer to the
libxine documentation. gxine is a GTK+ based GUI for this
xine-libraries alternat to xine-ui.

%description -l de
xine ist ein freies Audio- und Video-Abspielprogramm f�r unixartige
Systeme mit umfassenden Funktionen. Zur Audio- und Videodekodierung
und Wiedergabe werden die xine-Bibliotheken aus libxine verwendet.
Weitere Informationen �ber die unterst�tzten Formate entnehmen Sie in
der Dokumentation zu libxine. gxine ist eine GTK+ basierende grafische
Oberfl�che f�r diese xine-Bibliotheken, alternativ zur xine-ui

%description -l pl
xine to w pe�ni funkcjonalny wolnodost�pny odtwarzacz film�w dla
system�w uniksowych, korzystaj�cy z libxine do dekodowania i
odtwarzania d�wi�ku i obrazu. Wi�cej informacji o obs�ugiwanych
formatach mo�na znale�� w dokumentacji libxine. gxine to graficzny
interfejs u�ytkownika do tych bibliotek, oparty na GTK+, alternatywny
dla xine-ui.

%package -n browser-plugin-gxine
Summary:	gxine as browser plugin
Summary(pl):	gxine jako wtyczka przegl�darki
Group:		X11/Applications/Multimedia
Requires(post,postun):	browser-plugins >= 2.0
Requires:	%{name} = %{version}-%{release}
Requires:	browser-plugins(%{_target_base_arch})
Obsoletes:	mozilla-plugin-gxine

%description -n browser-plugin-gxine
gxine as browser plugin.

%description -n browser-plugin-gxine -l pl
gxine jako wtyczka przegl�darki.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_lirc:--disable-lirc} \
	--disable-static \
	--with-plugindir=%{_browserpluginsdir} \
	--with-spidermonkey=/usr/include/js

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	Applicationsdir=%{_desktopdir}

rm -f $RPM_BUILD_ROOT%{_browserpluginsdir}/*.la

%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post -n browser-plugin-gxine
%update_browser_plugins

%postun -n browser-plugin-gxine
if [ "$1" = "0" ]; then
	%update_browser_plugins
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO
%attr(755,root,root) %{_bindir}/gxine*
%{_datadir}/gxine
%dir %{_sysconfdir}/gxine
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/gxine/*
%{_desktopdir}/gxine.desktop
%{_iconsdir}/hicolor/*/*/*.png
%{_pixmapsdir}/gxine.png
%{_mandir}/man1/*
%lang(de) %{_mandir}/de/man1/*

%files -n browser-plugin-gxine
%defattr(644,root,root,755)
%attr(755,root,root) %{_browserpluginsdir}/gxineplugin.so

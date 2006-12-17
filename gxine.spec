# TODO: switch to browser-plugins
#
# Conditional build:
%bcond_without	lirc	# without LIRC support
#
Summary:	GTK+ based GUI for xine-libraries
Summary(de):	GTK+ basierende grafische Oberfläche für die xine-Bibliotheken
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
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	gtk+2-devel >= 1:2.6.0
BuildRequires:	js-devel
BuildRequires:	libtool
%{?with_lirc:BuildRequires:	lirc-devel}
BuildRequires:	nspr-devel
BuildRequires:	pkgconfig
BuildRequires:	xine-lib-devel >= 1:1.0
BuildRequires:	xorg-lib-libXaw-devel
Requires:	xine-lib >= 1:1.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		mozilladir	/usr/%{_lib}/mozilla/plugins

%description
xine is a fully-featured free audio/video player for unix-like systems
which uses libxine for audio/video decoding and playback. For more
informations on what formats are supported, please refer to the
libxine documentation. gxine is a GTK+ based GUI for this
xine-libraries alternat to xine-ui.

%description -l de
xine ist ein freies Audio- und Video-Abspielprogramm für unixartige
Systeme mit umfassenden Funktionen. Zur Audio- und Videodekodierung
und Wiedergabe werden die xine-Bibliotheken aus libxine verwendet.
Weitere Informationen über die unterstützten Formate entnehmen Sie in
der Dokumentation zu libxine. gxine ist eine GTK+ basierende grafische
Oberfläche für diese xine-Bibliotheken, alternativ zur xine-ui

%description -l pl
xine to w pe³ni funkcjonalny wolnodostêpny odtwarzacz filmów dla
systemów uniksowych, korzystaj±cy z libxine do dekodowania i
odtwarzania d¼wiêku i obrazu. Wiêcej informacji o obs³ugiwanych
formatach mo¿na znale¼æ w dokumentacji libxine. gxine to graficzny
interfejs u¿ytkownika do tych bibliotek, oparty na GTK+, alternatywny
dla xine-ui.

%package -n mozilla-plugin-gxine
Summary:	gxine as Mozilla plugin
Summary(pl):	gxine jako wtyczka Mozilli
Group:		X11/Applications/Multimedia
Requires:	%{name} = %{version}-%{release}

%description -n mozilla-plugin-gxine
gxine as Mozilla plugin.

%description -n mozilla-plugin-gxine -l pl
gxine jako wtyczka Mozilli.

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
	--with-plugindir=%{mozilladir} \
	--with-spidermonkey=/usr/include/js

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	Applicationsdir=%{_desktopdir}

rm -f $RPM_BUILD_ROOT%{mozilladir}/*.la

%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

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

%files -n mozilla-plugin-gxine
%defattr(644,root,root,755)
%attr(755,root,root) %{mozilladir}/gxineplugin.so

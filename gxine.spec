#
# Conditional build:
%bcond_without	lirc	# without LIRC support
#
Summary:	GTK+ based GUI for xine-libraries
Summary(de.UTF-8):	GTK+ basierende grafische Oberfläche für die xine-Bibliotheken
Summary(pl.UTF-8):	Oparty na GTK+ graficzny interfejs do bibliotek XINE
Name:		gxine
Version:	0.5.905
Release:	1
License:	GPL v2+
Group:		X11/Applications/Multimedia
Source0:	http://downloads.sourceforge.net/xine/%{name}-%{version}.tar.bz2
# Source0-md5:	3c9092f1c5c8dc85e95ca327cdcc77af
Patch0:		%{name}-desktop.patch
Patch1:		%{name}-plugindir.patch
Patch2:		%{name}-link.patch
URL:		http://www.xine-project.org/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.9
BuildRequires:	dbus-glib-devel >= 0.35
BuildRequires:	glib2-devel >= 1:2.10.0
BuildRequires:	gtk+2-devel >= 2:2.8.0
BuildRequires:	js-devel
BuildRequires:	libtool
BuildRequires:	libxcb-devel >= 1.0
%{?with_lirc:BuildRequires:	lirc-devel}
BuildRequires:	nspr-devel
BuildRequires:	pango-devel >= 1:1.12.0
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.357
BuildRequires:	udev-glib-devel
BuildRequires:	xine-lib-devel >= 2:1.1.8
BuildRequires:	xorg-lib-libXaw-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libXrandr-devel
BuildRequires:	xorg-lib-libXtst-devel
Requires:	glib2 >= 1:2.10.0
Requires:	gtk+2 >= 2:2.8.0
Requires:	pango >= 1:1.12.0
Requires:	xine-lib >= 2:1.1.8
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
xine is a fully-featured free audio/video player for unix-like systems
which uses libxine for audio/video decoding and playback. For more
informations on what formats are supported, please refer to the
libxine documentation. gxine is a GTK+ based GUI for this
xine-libraries alternat to xine-ui.

%description -l de.UTF-8
xine ist ein freies Audio- und Video-Abspielprogramm für unixartige
Systeme mit umfassenden Funktionen. Zur Audio- und Videodekodierung
und Wiedergabe werden die xine-Bibliotheken aus libxine verwendet.
Weitere Informationen über die unterstützten Formate entnehmen Sie in
der Dokumentation zu libxine. gxine ist eine GTK+ basierende grafische
Oberfläche für diese xine-Bibliotheken, alternativ zur xine-ui

%description -l pl.UTF-8
xine to w pełni funkcjonalny wolnodostępny odtwarzacz filmów dla
systemów uniksowych, korzystający z libxine do dekodowania i
odtwarzania dźwięku i obrazu. Więcej informacji o obsługiwanych
formatach można znaleźć w dokumentacji libxine. gxine to graficzny
interfejs użytkownika do tych bibliotek, oparty na GTK+, alternatywny
dla xine-ui.

%package -n browser-plugin-gxine
Summary:	gxine as browser plugin
Summary(pl.UTF-8):	gxine jako wtyczka przeglądarki
Group:		X11/Applications/Multimedia
Requires(post,postun):	browser-plugins >= 2.0
Requires:	%{name} = %{version}-%{release}
Requires:	browser-plugins(%{_target_base_arch})
Obsoletes:	mozilla-plugin-gxine

%description -n browser-plugin-gxine
gxine as browser plugin.

%description -n browser-plugin-gxine -l pl.UTF-8
gxine jako wtyczka przeglądarki.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	GSSCMD=/usr/bin/gnome-screensaver-command \
	XSSCMD=/usr/bin/xscreensaver \
	%{!?with_lirc:--disable-lirc} \
	--with-gudev \
	--with-plugindir=%{_browserpluginsdir} \
	--with-spidermonkey=/usr/include/js

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_browserpluginsdir}/*.la

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
%doc AUTHORS BUGS ChangeLog README TODO
%lang(cs) %doc README.cs
%lang(de) %doc README.de
%attr(755,root,root) %{_bindir}/gxine
%attr(755,root,root) %{_bindir}/gxine_client
%{_datadir}/gxine
%dir %{_sysconfdir}/gxine
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/gxine/gtkrc
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/gxine/startup
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/gxine/*.xml
%{_desktopdir}/gxine.desktop
%{_iconsdir}/hicolor/*/apps/gxine.png
%{_pixmapsdir}/gxine.png
%{_mandir}/man1/gxine.1*
%{_mandir}/man1/gxine_client.1*
%lang(de) %{_mandir}/de/man1/gxine.1*
%lang(de) %{_mandir}/de/man1/gxine_client.1*
%lang(es) %{_mandir}/es/man1/gxine.1*
%lang(es) %{_mandir}/es/man1/gxine_client.1*

%files -n browser-plugin-gxine
%defattr(644,root,root,755)
%attr(755,root,root) %{_browserpluginsdir}/gxineplugin.so

%define svn	3309
%define rel	1
%if %svn
%define release		%mkrel 0.%svn.%rel
%define distname	%name-%svn.tar.lzma
%define dirname		%name
%else
%define release		%mkrel %rel
%define distname	%name-%version.tar.gz
%define dirname		%name-%version
%endif

Name:		synce-kpm
Summary:	Graphical tool for managing Windows Mobile devices
Version:	0.11.1
Release:	%{release} 
Source0:	http://downloads.sourceforge.net/synce/%{distname}
URL:		http://www.synce.org/moin/SynceTools/SynceKpm
Group:		Communications
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
License:	GPLv2+
BuildArch:	noarch
BuildRequires:	python
BuildRequires:	python-devel
BuildRequires:	python-setuptools
Requires:	python-qt4
Requires:	odccm
Requires:	librapi-python


%description
SynCE-KPM stands for SynCE KDE PDA Manager and aims to be an
application to manage WM5/WM6 PDA devices from Linux. SynCE-KPM
provides the following features for managing your WM5/WM6 PDA from the
PC:

* Install / uninstall programs
* Display general device information
* Manage partnerships (in case sync-engine is installed and running)

%prep
%setup -q -n %{dirname}

%build
%{__python} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install --root=%{buildroot} --compile --optimize=2

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS Changelog README TODO
%{_bindir}/%{name}
%{py_puresitedir}/synceKPM
%{py_puresitedir}/synce_kpm-0.11-py%{pyver}.egg-info


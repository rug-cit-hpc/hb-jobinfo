Name: hb-jobinfo
Version: HB_JOBINFO_VERSION
Release: 1%{?dist}
Summary: Collect job information from SLURM in nicely readable format.
Obsoletes: jobinfo <= 2.1.0

Group: System Environment/Base
License: MIT
URL: https://github.com/rug-cit-hpc/hb-jobinfo
Source0: %{name}-%{version}.tar.gz
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: python3 %{py3_dist requests}
BuildRequires:  python%{python3_pkgversion}-devel

%description
jobinfo - collates job information from the 'sstat', 'sacct' and 'squeue' SLURM commands to give a uniform interface for both current and historical jobs.

%prep
%setup -q

%build
#make

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{python3_sitelib}
install jobinfo %{buildroot}%{_bindir}/jobinfo

%files
%defattr(-,root,root)
%{_bindir}/jobinfo

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Wed Apr 26 2024 Fokke Dijkstra <f.dijkstra@rug.nl> - 1.0.0
- First version of the rewritten tool

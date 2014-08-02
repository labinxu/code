@rem Author: ext-laibin.xu@nokia.com
@rem trigger ut test for app gallery2 --tests_proj_filter "Gallery2"
cd %~pd0

call python autotrigger.py --submit "True" --product "athena" --icase_mode "icase" --icase_svn_rel "" --target_build_variant "eng" --testtype "ut_autotrigger_ut" --tests_proj_filter "Gallery2" --gerrit_project ""
choice /t 15 /d y /n >nul
@rem trigger self rfa
call python autotrigger.py --submit "True" --product "athena" --icase_svn_rel "" --target_build_variant "eng" --testtype "rfa_autotriger" --icase_index "testcloud_self_run_index" --icase_mode "test_automation/system_tests/RFA" --icase_path "tools/test_automation" --gerrit_project "tools/test_automation"
choice /t 15 /d y /n >nul
@rem trigger split
call python autotrigger.py --submit "True" --product "athena" --icase_svn_rel "" --target_build_variant "eng" --testtype "rfa_autotrigger_split" --icase_index "marble_rfa_all_index" --icase_mode "test_automation/system_tests/RFA" --icase_path "tools/test_automation" --icase_split "3" --gerrit_project "tools/test_automation"
pause


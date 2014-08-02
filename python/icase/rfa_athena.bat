echo off
cd %~pd0
:loop
@rem if %time:~0,5% == 10:34 (goto doSomething)
goto rfaTrigger
:backrfaTrigger

goto end

@rem Author: ext-laibin.xu@nokia.com
@rem trigger ut test for app gallery2 --tests_proj_filter "Gallery2"
:utTrigger
echo utTrigger
@rem call python autotrigger.py --submit "True" --product "lybra" --icase_mode "icase" --icase_svn_rel "" --target_build_variant "eng" --testtype "ut_autotrigger_ut" --tests_proj_filter "Gallery2"
goto backutTrigger

:rfaTrigger
echo rfaTrigger
@rem trigger self rfa
call python autotrigger.py --submit "True" --product "athena" --icase_svn_rel "" --target_build_variant "eng" --testtype "anthena_marble_rfa_all_index" --icase_index "testcloud_self_run_index" --icase_mode "test_automation/system_tests/RFA" --icase_path "tools/test_automation" 
goto backrfaTrigger

:rfaSplitTrigger
echo rfaSplitTrigger
@rem trigger split
@rem call python autotrigger.py --submit "True" --product "athena" --icase_svn_rel "" --target_build_variant "eng" --testtype "rfa_autotrigger_split" --icase_index "marble_rfa_all_index" --icase_mode "test_automation/system_tests/RFA" --icase_path "tools/test_automation" --icase_split "3"
goto backrfaSplitTrigger


:end
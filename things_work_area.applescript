(*

Toggle the suspended status of an area thing things.

I don't want to see my "work" area appearing on the weekends, so I
create a cron job to disable the area temporarily and then reenable it
on Monday morning.

  0 10 * * 1 osascript things_work_area.osascript
  0 19 * * 5 osascript things_work_area.osascript
*)

tell application "Things"
	set work_ar to area named "Work"
	if (get suspended of work_ar) then
		set suspended of work_ar to false
	else
		set suspended of work_ar to true
	end if

end tell
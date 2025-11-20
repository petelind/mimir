Design the Playbook (FOB):
- use UI to design the playbook
- encode my notes into the structured playbook (windsurf/cursos workflow provided for you)
- use MCP to create a new playbook [from the structured playbook we just created]
- use MCP to put stuff into the playbook
- send to the Homebase to the Family
- send to the Homebase for Private use

Publish the Playbook (Homebase):
- Author can specify if he wants to share and which Families(Tiers if its a commercial service) to share with
- Admin can approve the playbook and it will be availabe for download from Homebase to FOBs
- Admin can register a new Family(Tier if its a commercial service)
- Family may or may not require approval to join
- Admin can add/remove people to/from the Family
- Admin can approve/reject/inactivate the playbook
- Admin can force-remove playbooks (on next update any FOB will remove it)

Operating on the FOB:
I can run FOB with Homebase or operate on my own
When on my own:
- I can load playbooks from dump
- I can enable/disable playbooks
- I can dump playbooks to dump to distribute to other FOBs
+ Design the playbook section (except for the "send to the homebase" part)
- I can register on the Homebase

When I have Homebase:
- I can join/leave the family(s) - I can belong to more than one
- I can start a new Family and become its admin
- If I'm family admin I can add/remove people to/from the Family
- If I'm family admin I can approve/reject/inactivate the playbooks submitted to that family
- If I'm family admin I can force-remove playbooks (on next update any FOB will remove it)
- If I'm family admin I can delete the family
- If I'm family admin I can transfer admin to someone else
- If I'm family admin I can edit family properties and desc
- If I'm family admin I can hide the family so only I can see it and will not appear anywhere (you have to be added by me to take part in it)
- If I'm family admin I can make the family public so anyone can join
- If I'm family admin I can deactivate the family - it will be hidden from the list and will not appear anywhere, and all family's playbooks will be force-removed from the FOBs
- I can see the list of available playbooks from Homebase I'm entitled to
- I can download the playbooks to FOB
- I can upload the playbooks to Homebase
- I can upload IMPROVED playbooks to Homebase (run diff between FOB and Homebase Playbook's versions; and upload only the changes as PIPs to the current version on the Homebase)
- I can delete my own the playbooks
- I can update the playbooks
- I can approve/reject/inactivate the playbook

Using Playbooks on FOB:
- I can select a playbook ("Activate UX playbook, lets work on the screen flow.)
- I can run MCP and query contentn ("Tell me how do I create screenflow?")
- I can run MCP to create a Work Item following playbook ("Lets create a plan for the Mimir screen flow per UX1 and put it into GitHub issue")
- I can work with Work Item following the playbook ("Lets pickup MIMR-1234 - assess the codebase and identify whats next per FF playbook? What do we do next?")
- I can run MCP to submit a PIP to the playbook ("Lets suggest that we need gradual progression for the screenflow: from workflow diagram to the wireframes to the hi-fi designs. I think its shall be right after UX1, adding 3 extra steps. Lets detail it in the PIP.")
- AI can submit PIPs to the playbook ("MIMR-1234Done; committed, merged, pushed. By the way: you are repeatedly stating primary controls placement. I think we need to update IA_guidelines Howto to include section for the primary control placement. Do you want me to submit PIP for it?")
- I can approve/reject/changes PIPs submitted to the playbook ("Approve PIP we just created; makes total sense to me.")
- I can ask MCP to open specifics of the Activity/Artifact/Goal etc. ("I want to see this UX worfklow in its entirety. Open the page.") - system will open web interface and navigate to the page: note that its important to structure URLs to allow that; we need to update @SAO.MD.

---

## Questions to Denis

### 1. PIP Lifecycle & Workflow
**Q:** PIPs are submitted on FOB, but how do they reach Homebase? Is there an explicit "submit PIP to Homebase" action, or does it happen automatically when syncing?

**A:** 
They do not. I submit PIPs to the playbook on FOB, and then I try to upload NEW PIP to Homebase (essentiall create new PIP on the Homebase) reconciling my version of the methodology and theirs.
---

**Q:** Who reviews and approves PIPs on Homebase - the original playbook author? Family admin? Both? What's the approval workflow?

**A:** 
Anyone with the admin rights on the Homebase can approve/reject PIPs. If it goes to family - family admin can also do that.

---

**Q:** How do approved PIPs get merged into the main playbook version? Is this automatic upon approval, or does the author need to explicitly merge them?

**A:** 
New PIP is essentially a) modified version of the Entity we have in the playbook or b) extension of the playbook - new Activity/Artifact/Goal etc. with new links (for example, new activity with the new "upstream" and "downstream" links)

---

### 2. Playbook Versioning & Sync
**Q:** When a playbook updates on Homebase, how do FOBs learn about it? Is sync automatic, manual check, or push notification-based?

**A:** 
its pull/push process:
1. FOB connects to the Homebase.
2. Homebase tells which playbooks this user is entitled to and their current version.
3. FOB compares versions and asks user if he wants to donwnload updates. If there is local change (for example, FOB updated local UX v19 to UX v19.1 and remote is UX v20) - FOB will ask user to resolve the conflict in a blunt manner - who takes precedence, and overwrite the other (no merging just yet).
---

**Q:** What happens when there are conflicts between local FOB changes and Homebase updates? Can users pin to specific playbook versions, or do they always get the latest?

**A:** 
See above.

---

### 3. Family Membership Workflow
**Q:** When a user requests to join a family requiring approval, where do they see their request status (pending/approved/rejected)?

**A:** 
Depends on the Family settings: family can be set to auto-approve or require approval.
We use django admin interface to manage family members and approvals/statuses (think like this - family is a Django group).
---

**Q:** Where do family admins review and approve/reject join requests?

**A:** 
See above.
---

**Q:** When a user is removed from a family, what happens to the playbooks they've already downloaded from that family?

**A:** 
Force-removed on next sync.
---

### 4. Private vs. Family Playbooks
**Q:** What's the difference between "send to Homebase to the Family" vs. "send to Homebase for Private use"? Who can see/access private playbooks?

**A:** 
Private playbooks are visible only to the user who uploaded them.
---

**Q:** Can a private playbook later become a family playbook, or is this decision final at upload time?

**A:** 
Yes; and it can be removed from the family.
---

### 5. Playbook Ownership & Control
**Q:** Who "owns" a playbook on Homebase - the author or the family? If an author leaves a family, what happens to playbooks they created?

**A:** 
If its private - author, if its family - family admin. But author can recall the playbook to private. And author can release authorship (think "I created private playbook and sold to you; now its your property")
---

**Q:** Can family admins edit playbooks directly, or can they only approve/reject them?

**A:** 
Family admin can approve/reject PIPs submitted to the playbook, and edit them.

---

**Q:** Can authors withdraw their playbooks from families after they've been approved?

**A:** 
Yes. Same if they were kicked off from the family - playbooks they submitted are no longer family's to use. Want them back? Buy them.
---

### 6. Discovery Mechanisms
**Q:** How do users discover families? Is there a browse/search interface, or is it invite-only? Can users see family descriptions before joining?

**A:** 
Browse/search interface with family descriptions, join requests, and approval workflow.

---

**Q:** How do users discover and browse playbooks? Can they search/filter by categories, tags, or keywords? Can they preview playbooks before downloading?

**A:** 
Yes. We have prototype for this already.
---

### 7. Notification System
**Q:** What notifications should users receive? (e.g., new playbooks in family, playbook updates, PIP submissions, join requests for admins, approval/rejection status, etc.)

**A:** 
All of that. We need simple notification system + icon on the toolbar with badge count + simple reader with dismiss button + signalling creating these notifications on the Playbook/Family/User related CUD events; like "New user want to join the Family; links to view/approve/reject"  .
---

### 8. Offline/Sync Behavior
**Q:** When FOB operates offline, what functionality is available? Can users still create work items, submit PIPs locally, and query playbook content?

**A:** 
Everything is available - sync just updates local graph.
---

**Q:** When FOB reconnects to Homebase, how does sync work? How are conflicts resolved (e.g., if a playbook was updated both locally and on Homebase)?

**A:** 
See above.
---

### 9. Playbook Lifecycle on FOB
**Q:** What's the difference between "disable" and "delete" for playbooks on FOB? Can disabled playbooks be re-enabled?

**A:** 
Disabled playbooks are not available in the UI, but they do exist in the graph. Deleted playbooks are removed.
---

**Q:** When a playbook is removed (deleted or force-removed), what happens to associated work items? Are they archived, deleted, or orphaned?

**A:** 
Work items are not created in the Playbook/Mimir system! You have to use your MCP to create them -eg Github/Atlassian/Gitlab whatever.

---

### 10. Work Item Management
**Q:** Is there a way to view all work items across all playbooks? Can users filter/search work items, or are they only accessible within the context of a specific playbook?

**A:** 
Work items are not created in the Playbook/Mimir system! You have to use your MCP to create them -eg Github/Atlassian/Gitlab whatever.

---

**Q:** Can users archive completed work items? How are archived vs. active work items distinguished?

**A:** 
Work items are not created in the Playbook/Mimir system! You have to use your MCP to create them -eg Github/Atlassian/Gitlab whatever.

---

### 11. Role Clarifications
**Q:** In "Operating on the FOB" > "When I have Homebase" section, you list family admin capabilities again. Are these the same actions as in "Publish the Playbook", or are they different (FOB-initiated vs. Homebase-initiated)?

**A:** 
Same.

---

### 12. Clarification Needed
**Q:** Line 24 has "+ Design the playbook section (except for the 'send to the homebase' part)" - is this a note/TODO or part of the user journey flow?

**A:** 
Its a reference to the section above (kinda means "this and whats in that section").


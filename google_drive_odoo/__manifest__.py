# -*- coding: utf-8 -*-
{
    "name": "Google Drive Odoo Integration",
    "version": "13.0.1.1.8",
    "category": "Document Management",
    "author": "Odoo Tools",
    "website": "https://odootools.com/apps/13.0/google-drive-odoo-integration-426",
    "license": "Other proprietary",
    "application": True,
    "installable": True,
    "auto_install": False,
    "depends": [
        "cloud_base"
    ],
    "data": [
        "data/data.xml",
        "security/ir.model.access.csv",
        "views/res_config_settings.xml"
    ],
    "qweb": [
        
    ],
    "js": [
        
    ],
    "demo": [
        
    ],
    "external_dependencies": {
        "python": []
},
    "summary": "The tool to automatically synchronize Odoo attachments with Google Drive files in both ways",
    "description": """
    This is the tool to integrate Google Drive features into your Odoo business work flow. The app automatically stores Odoo attachments in Google Drive, and it provides an instant access to them via web links. In such a way users work with files comfortably in the cloud storage, while the results are fully available in Odoo.<br/>
The tool work is guaranteed by a few apps:

    Selectable documents types for sync
    Automatic and bilateral integration
    Direct access to Google Drive items
    Individual and team drives
    Fully integrated and compatible with Enterprise Documents
    Google Drive Sync logs in Odoo
    Default folders for documents
    # Typical use cases
    <ul style='font-size:18px;'>
<li><i>Projects:</i> have an own Google Drive folder for each customer project.</li>
<li><i>Customers</i>: add all partner files in a single directory available both from Odoo and from Google Drive. Modify those using default cloud editors and access them when working in Odoo.</i></li>
<li><i>Employees:</i> gather all files by this employee in a single cloud folder: photos, document scans, contracts. Access and upload those from Odoo and Google Drive alternatively.</li>
<li><i>Opportunities:</i> carefully store all specifications, requirements, any files which would let you make a good offer.</li>
<li><i>Orders:</i> keep all printings and contracts in Google Drive with simple availability from Odoo.</li>
</ul>
    # How files and folders are synced from Odoo to Google Drive
    <p style="font-size:18px">
Based on the scheduled job 'Synchronize attachments with cloud' Odoo regularly checks whether:
</p>
<ul style="font-size:18px">
<li>Any new attachment should be forwarded to Google Drive;</li>
<li>Any new document type (e.g. Sale orders) is added / replaced / renamed as a sync model and, hence, whether a directory should be created / removed / renamed in Google Drive;</li>
<li>Any new document (e.g. Sale Order SO019) is generated / updated / unlinked and, hence, whether a Google Drive folder should be created / moved or renamed / deleted.</li>
<li>Any new attachment should be removed from Google Drive if it has been deleted from Odoo.</li>
</ul>
<p style="font-size:18px">
Based on results of that checks, Odoo starts processing queue of changes, and makes sure that all items are located correctly. The final goal is to have the structure 'Odoo / Document Types / Documents / Files. For example, 'Odoo / Quotations / SO019 / commercial offer.pdf'.
</p>
<p style="font-size:18px">
During the synchronization all synced Odoo attachments change their type to a link (URL), while binary content is removed with a next Odoo cleaner. So, no actual files would be stored on your Odoo server.
</p>
<p style="font-size:18px">
Please take into account:
</p>
<ul style="font-size:18px">
<li>Each sync (especially the very first one) might take quite a long. It is not recommended to make sync too frequent: once an hour seems reasonable frequency.</li>
<li>File names should be managed in Google Drive: each backward sync would recover Google Drive names, Odoo is here less important.</li>
</ul>
    # How items are retrieved from Google Drive to Odoo
    <p style="font-size:18px">
Based on the scheduled job 'Synchronize attachments from cloud' Odoo regularly checks whether:
</p>
<ul style="font-size:18px">
<li>Any file is added / moved / removed in a Google Drive document folder. If yes, Odoo would create a link to this file in a target object (e.g. a new attachment to SO019) or would move / delete such an attachment.</li>
<li>Any file of a Google Drive document folder is renamed. If yes, an attachment would be renamed in Odoo as well.</li>
</ul>
Please take into account:
</p>
<ul style="font-size:18px">
<li>In document folders you can put not only files but also child folders. In that case a link for this folder (not its content) would be kept in Odoo attachments.</li>
<li>If you deleted a folder related to this document type or this document, their child files would be deleted as well. Thus, Odoo would remove related attachments. The folders, however, will be recovered with a next direct sync.</li>
<li>Each backward sync might take quite a long. It is not recommended to make sync too frequent: once an hour seems safe enough.</li>
</ul>
    # <i class='fa fa-folder-open'></i> How Odoo Enterprise Documents are synced
    <p style="font-size:18px">
This tool is not in conflict with the 'documents' module provided under the Enterprise license. Attachments related to Enterprise folders would be synced as any other files: according to a document they relate to.
</p>
<p style="font-size:18px">
It is not always comfortable, and you might be interested in reflecting directories' structure introduced by the module 'Documents'. To this end the special extension is developed. This extension introduces the following features:
</p>
<ul style="font-size:18px">
<li>The documents hierarchy is reflected within the folder 'Odoo / Odoo Docs'</li>
<li>Each Odoo folder has a linked cloud folder. Take into account that folders created in the cloud storage will be synced as Odoo attachments. The key principle is: folders are managed by Odoo, files are managed by the cloud client</li>
<li>All files are synced with the same logic as usual attachments. Files created in Odoo will be added to the cloud storage and will be replaced with links in Odoo. Files created in cloud storage will generate attachments within a paired directory</li>
<li>Please do not name synced models as 'Odoo Docs'. This is the reserved name for Odoo Enterprise Documents</li>
</ul>
    # A few important peculiarities to take into account
    <ul>
<li>Take into account that files or folders deleted in Google Drive are really deleted only when you clean trash. Otherwise, such files still exist and would be reflected in Odoo</li>
<li>Try to avoid the following symbols in folders' and files' names: *, ?, ", ', :, &lt;, &gt;, |, +, %, !, @, \, /,.  Direct sync will replace such symbols with '-'. It is done to avoid conflicts with file systems.</li>
</ul>
    Quick access to Google Drive files and folders
    Apply to Google Drive right from Odoo chatter
    Choose document types to be synced
    Document type might have a few folders based on filters
    Synced files are simply found in Google Drive. Add unlimited number of files or folders
    Document types folders in Google Drive
    All document of this type has an own folder
    Direct access from Odoo documents to Google Drive
    Enterprise Documents in Google Drive
    Enterprise files in Google Drive
    Logged synchronization activities
    I faced the error: QWeb2: Template 'X' not found
    <div class="knowsystem_block_title_text">
            <div class="knowsystem_snippet_general" style="margin:0px auto 0px auto;width:100%;">
                <table align="center" cellspacing="0" cellpadding="0" border="0" class="knowsystem_table_styles" style="width:100%;background-color:transparent;border-collapse:separate;">
                    <tbody>
                        <tr>
                            <td width="100%" class="knowsystem_h_padding knowsystem_v_padding o_knowsystem_no_colorpicker" style="padding:20px;vertical-align:top;text-align:inherit;">
                                
                                <ol style="margin:0px 0 10px 0;list-style-type:decimal;"><li><p class="" style="margin:0px;">Restart your Odoo server and update the module</p></li><li><p class="" style="margin:0px;">Clean your browser cache (Ctrl + Shift + R) or open Odoo in a private window.</p></li></ol></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    What are update policies of your tools?
    
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


<p style="margin:0px 0px 0.25cm 0px;line-height:120%;">
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


</p><p style="margin:0px 0px 0.25cm 0px;line-height:120%;">
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


</p><p style="margin:0px 0px 0.25cm 0px;line-height:120%;">
	
	
	<style type="text/css">
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 115% }
	</style>


</p><p lang="en-US" style="margin:0px 0px 0.25cm 0px;line-height:120%;">According to the current Odoo Apps Store policies:</p><ul style="margin:0px 0 10px 0;list-style-type:disc;"><li><p lang="en-US" style="margin:0px;line-height:120%;"> every module bought for the version 12.0 and prior gives you an access to the all versions up to 12.0. </p></li><li><p lang="en-US" style="margin:0px;line-height:120%;">starting from the version 13.0, every version of the module should be purchased separately.</p></li><li><p lang="en-US" style="margin:0px;line-height:120%;">disregarding the version, purchasing a tool grants you a right for all updates and bug fixes within a major version.<br></p></li></ul><p lang="en-US" style="margin:0px 0px 0.25cm 0px;line-height:120%;">Take into account that Odoo Tools team does not control those policies. By all questions please contact the Odoo Apps Store representatives <a href="https://www.odoo.com/contactus" style="text-decoration:none;color:rgb(13, 103, 89);background-color:transparent;">directly</a>.</p>
    May I buy your app from your company directly?
    
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


<p style="margin:0px 0px 10px 0px;">Sorry, but no. We distribute the
tools only through the <a href="https://apps.odoo.com/apps" style="text-decoration:none;color:rgb(13, 103, 89);background-color:transparent;">official Odoo apps store</a></p>
    How should I install your app?
    
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


<p style="line-height:120%;margin:0px 0px 10px 0px;">
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


</p><ol style="margin:0px 0 10px 0;list-style-type:decimal;">
	<li><p style="margin:0px;line-height:120%;">Unzip source code of purchased tools in one of your Odoo
	add-ons directory</p>
	</li><li><p style="margin:0px;line-height:120%;">Re-start the Odoo server</p>
	</li><li><p style="margin:0px;line-height:120%;">Turn on the developer mode (technical settings)</p>
	</li><li><p style="margin:0px;line-height:120%;">Update the apps' list (the apps' menu)</p>
	</li><li><p style="margin:0px;line-height:120%;">Find the app and push the button 'Install'</p>
	</li><li><p style="margin:0px;line-height:120%;">Follow the guidelines on the app's page if those exist.</p>
</li></ol>
    Can I have a few folders for the the same document type? For example, internal projects and customer projects?
    
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


<p style="line-height:120%;margin:0px 0px 10px 0px;">Yes, you can. To that goal you should prepare a separate sync
model on the configuration tab. Then, for each of those apply
filters: for example by type of a project.</p>
<p style="line-height:120%;margin:0px 0px 10px 0px;">Try to make filters self-exclusive in order a document can be
definitely assigned. For instance, 'customer but not supplier',
'supplier but not customer'. Otherwise, a specific document folder
would jump from one model to another.</p>
    Your tool has dependencies on other app(s). Should I purchase those?
    
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


<p style="margin:0px 0px 0.25cm 0px;line-height:120%;">Yes, all modules marked in dependencies are absolutely required for a correct work of our tool. Take into account that price marked on the app page already includes all necessary dependencies.&nbsp;&nbsp;</p>
    May I change frequency of sync jobs?
    
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


<p style="margin:0px 0px 0.25cm 0px;line-height:120%;">Yes, you can. To this end:</p><ol style="margin:0px 0 10px 0;list-style-type:decimal;"><li><p style="margin:0px;line-height:120%;">Turn on debug mode</p></li><li><p style="margin:0px;line-height:120%;">Go to technical settings &gt; Automation &gt; Scheduled jobs</p></li><li><p style="margin:0px;line-height:120%;">Find the jobs 'Synchronize attachments with cloud' and 'Update attachments from cloud'.</p></li></ol><p style="margin:0px 0px 0.25cm 0px;line-height:120%;">Take into account that you should not make them too frequent. It would be better if that this job should be finished until a new one is started. Thus, the configuration should depend on how many items you to sync you have. Usually, the frequency is set up between 10 minutes to 4 hours.</p><p style="margin:0px 0px 0.25cm 0px;line-height:120%;">Make also sure that you have set up enough time limits in your
Odoo configuration file. Thus, LIMIT_TIME_CPU and LIMIT_TIME_REAL
parameters should be equal or bigger than planned cron job time.</p><p style="line-height:120%;margin:0px 0px 10px 0px;">
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>










</p><p style="margin:0px 0px 0.25cm 0px;line-height:120%;">An import notice for Odoo.sh clients: the maximum time for cron
job might be set up as 15 minutes.</p>
    I noticed that your app has extra add-ons. May I purchase them afterwards?
    
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


<p style="margin:0px 0px 0.25cm 0px;line-height:120%;">
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


</p><p style="margin:0px 0px 0.25cm 0px;line-height:120%;">Yes, sure. Take into account that Odoo
automatically adds all dependencies to a cart. You should exclude
previously purchased tools.</p>
    I would like to get a discount
    
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


<p style="margin:0px 0px 0.25cm 0px;line-height:120%;">
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


</p><p style="margin:0px 0px 0.25cm 0px;line-height:120%;">
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


</p><p style="margin:0px 0px 0.25cm 0px;line-height:120%;">
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


</p><p style="margin:0px 0px 0.25cm 0px;line-height:120%;">Regretfully, we do not have a
technical possibility to provide individual prices.</p>
    Would the app work with the Odoo Enterprise Documents app? 
    
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


<p style="margin:0px 0px 0.25cm 0px;line-height:120%;">
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


</p><p style="margin:0px 0px 0.25cm 0px;line-height:120%;">For Odoo v12 Enterprise you have 2 options:</p><p style="margin:0px 0px 0.25cm 0px;line-height:120%;">
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>



</p><ol style="margin:0px 0 10px 0;list-style-type:decimal;">
	<li><p style="margin:0px;line-height:120%;">To sync only standard documents' attachments, but not to sync
	folders' and files' structure related to the Enterprise module
	'Documents'.</p>
	</li><li><p style="margin:0px;line-height:120%;">To sync both Odoo standard attachments and to reflect
	Enterprise Documents' folders/files. In such a case you need an
	extra add-in <a href="https://apps.odoo.com/apps/modules/12.0/cloud_base_documents/" style="text-decoration:none;color:rgb(13, 103, 89);background-color:transparent;">Cloud
	Sync for Enterprise Documents</a> (44 Euro).</p>
</li></ol>
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


<p style="margin:0px 0px 0.25cm 0px;line-height:120%;">
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


</p><style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>
    Is it possible to make synchronization real-time?
    
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


<p style="margin:0px 0px 0.25cm 0px;line-height:120%;">
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


</p><p style="margin:0px 0px 0.25cm 0px;line-height:120%;">No. We have strong reasons to avoid real time sync:</p><p style="margin:0px 0px 0.25cm 0px;line-height:120%;">
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>




</p><ul style="margin:0px 0 10px 0;list-style-type:disc;">
	<li><p style="margin:0px;line-height:120%;">Performance issues. In case a sync is real time, each file
	upload will result in the loading screen.</p>
	</li><li><p style="margin:0px;line-height:120%;">Conflict issues. If 2 users simultaneously change an item, it
	might lead to unresolved situations. In case of regular jobs we can
	fix it afterwards, while in case of real time we would need to save
	it as some queue, and it will be even more misleading for users.</p>
	</li><li><p style="margin:0px;line-height:120%;">Functionality issues. In particular, renaming and
	restructuring of items. In the backward sync the tool strictly
	relies upon directories' logic, and during each sync 100% of items
	are checked. In case it is done after each update, it will be
	thousands of requests per second. If not: changes would be lost.</p>
</li></ul><style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>
    Should I set up specific users accesses in Odoo?
    
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


<p style="margin:0px 0px 0.25cm 0px;line-height:120%;">No, the tool relies upon a single user end point. It means that
all sync processes are done under a single cloud admin (app). Access
rights for created folders / files are not automatized. You should
administrate those rights in your cloud storage solution.</p>
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


<p style="margin:0px 0px 0.25cm 0px;line-height:120%;"><style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style></p>
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


<p style="margin:0px 0px 0.25cm 0px;line-height:120%;">
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


</p><style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>
    How can I install your app on Odoo.sh?
    
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


<p style="margin:0px 0px 10px 0px;">As soon as you purchased the
app, the button 'Deploy on Odoo.sh' will appear on the app's page in
the Odoo store. Push this button and follow the instructions.</p>
<p style="margin:0px 0px 10px 0px;">Take into account that for paid
tools you need to have a private GIT repository linked to your
Odoo.sh projects</p>
    May I install the app on my Odoo Online (SaaS) database?
    <p style="margin:0px 0px 10px 0px;">No, third party apps can not be used on Odoo Online.</p>
    Where would be synced fields stored? Are they duplicated to Odoo and clouds?
    
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


<p style="margin:0px 0px 0.25cm 0px;line-height:120%;">
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


</p><p style="margin:0px 0px 0.25cm 0px;line-height:120%;">All synced files are kept only in the clouds, in Odoo attachments
become of the URL-type. When a user clicks on those, Odoo would
redirect him/her to a cloud storage.</p><style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>
    Is it Okay if I had many objects to sync, for example, 10000?
    
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


<p style="margin:0px 0px 0.25cm 0px;line-height:120%;">Yes, although in case of many folders / attachments to sync, the
process might be slow. Simultaneously, our clients reported to us the
environments with &gt;10k partners and ~5k product variants to be
synced, and the processes were acceptable.</p>
<p style="margin:0px 0px 0.25cm 0px;line-height:120%;">A few points to emphasize:</p>
<ol style="margin:0px 0 10px 0;list-style-type:decimal;">
	<li><p style="margin:0px;line-height:120%;">The sync is constructed in such a way that anyway any item
	will be synced and will not be lost, although it might be not fast.
	It is guaranteed by first-in-first-out queues and by each job
	commits.</p>
	</li><li><p style="margin:0px;line-height:120%;">The number of objects might be limited logically. The models'
	configuration let you restrict sync of obsolete items (e.g there is
	no sense to sync archived partners or orders which are done 2 years
	ago).</p>
</li></ol>
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


<p style="margin:0px 0px 0.25cm 0px;line-height:120%;">
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


</p><style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>
    Would standard Odoo preview work for synced items?
    
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


<p style="margin:0px 0px 0.25cm 0px;line-height:120%;">
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


</p><p style="margin:0px 0px 0.25cm 0px;line-height:120%;">No, since files are now kept in the cloud storage, and retrieving
binary contents would consume a lot of resources. Odoo has a link
which would redirect a user to a proper previewer or editor.</p>
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


<p style="margin:0px 0px 0.25cm 0px;line-height:120%;">
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


</p><style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>
    May I change default folders' name in clouds?
    
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


<p style="margin:0px 0px 0.25cm 0px;line-height:120%;">For models' directories (sale orders, opportunities, suppliers,
etc.): you may assign your own name on the configuration tab for any
document type.</p><p style="margin:0px 0px 0.25cm 0px;line-height:120%;">
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>



</p><p style="margin:0px 0px 0.25cm 0px;line-height:120%;">For objects' folders (SO-001, John Smith, etc.): the tool relies
upon the Odoo 'name_get' method for this document type. In case you
need to make a different title, you should re-define this method for
a specific model. It requires source code modification.</p>
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


<p style="margin:0px 0px 0.25cm 0px;line-height:120%;"><style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style></p>
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


<p style="margin:0px 0px 0.25cm 0px;line-height:120%;">
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


</p><style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>
    May I configure different structure of synced directories rather than assumed by sync?
    
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


<p style="margin:0px 0px 0.25cm 0px;line-height:120%;">No, the module works with the pre-defined structure of folders:</p><ol style="margin:0px 0 10px 0;list-style-type:decimal;">
	<li><p style="margin:0px;line-height:120%;">Odoo – a core folder for sync</p>
	</li><li><p style="margin:0px;line-height:120%;">Models – folders for each Odoo document type. For example,
	'Projects', 'Partners'. Distinguished by domain there might be more
	specific folders: e.g., 'Customer 1 Projects', 'Projects of the
	Customer 2', 'Internal Projects', etc.</p>
	</li><li><p style="margin:0px;line-height:120%;">Objects – folders for each document, e.g. 'Project 1' or
	'Customer 1'</p>
	</li><li><p style="margin:0px;line-height:120%;">Files and folders related to this Odoo document to be synced.</p>
</li></ol><p style="margin:0px 0px 0.25cm 0px;line-height:120%;">As a result you may have for instance:</p><ul style="margin:0px 0 10px 0;list-style-type:disc;">
	<li><p style="margin:0px;line-height:120%;">Odoo / Projects / Project 1 / files and folders related to
	the&nbsp; project 1</p>
	</li><li><p style="margin:0px;line-height:120%;">Odoo / Customer 1 Projects / Project 1; Odoo / Customer 2
	Projects / Project 3, ...</p>
	</li><li><p style="margin:0px;line-height:120%;">Odoo / Customers / Customer 1 / files and folders related to
	the customer 1</p>
</li></ul><p style="margin:0px 0px 0.25cm 0px;line-height:120%;">
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>






</p><p style="margin:0px 0px 0.25cm 0px;line-height:120%;">This structure is always flat, meaning that there are only those
levels of hierarchy. Thus, it is correct that various document types
can't be done within the same structure. Within the folder 'Customer
1' we can't keep the files related both to sale orders, invoices, and
projects. Each of those document type has an own (or a few own)
folders. Otherwise, we will not have a chance to make backward
synchronisation, since there would be no criteria to rely upon.</p>
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


<p style="margin:0px 0px 0.25cm 0px;line-height:120%;"><style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style></p>
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


<p style="margin:0px 0px 0.25cm 0px;line-height:120%;">
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


</p><style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style><style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>
    Do I need only the Cloud Storage Solution app?
    
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


<p style="margin:0px 0px 0.25cm 0px;line-height:120%;">
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


</p><p style="margin:0px 0px 0.25cm 0px;line-height:120%;">No, the tool is only a technical core. You also need the connector
for your cloud client.</p>
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


<p style="margin:0px 0px 0.25cm 0px;line-height:120%;"><style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style></p>
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


<p style="margin:0px 0px 0.25cm 0px;line-height:120%;">
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


</p><style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style><style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>
    We use a special editor in our clouds (e.g. OnlyOffice, Office 365, etc.). Would files be opened in that editor?
    
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


<p style="margin:0px 0px 0.25cm 0px;line-height:120%;">
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


</p><p style="margin:0px 0px 0.25cm 0px;line-height:120%;">
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


</p><p style="margin:0px 0px 0.25cm 0px;line-height:120%;">Yes, depending on your cloud client configuration.</p>
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


<p style="margin:0px 0px 0.25cm 0px;line-height:120%;"><style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style></p>
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


<p style="margin:0px 0px 0.25cm 0px;line-height:120%;">
	
	
	<style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>


</p><style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style><style type="text/css">
	<!--
		@page { margin: 2cm }
		p { margin-bottom: 0.25cm; line-height: 120% }
		a:link { so-language: zxx }
	-->
	</style>
""",
    "images": [
        "static/description/main.png"
    ],
    "price": "264.0",
    "currency": "EUR",
}
Þ          \  µ         p  9  q  6  «  r  â  <   U          ¬     º     Ú      ø          9  "   Y     |  ;        Î     è  /      7   0  J   h  H   ³     ü     
                5     F  	   M     W     p     x  
     
                  ª     ³  	   ¼     Æ     Ë  -   Ñ  "   ÿ     "  j   /               ¥     ®     ¾     Ô  	   ä  	   î     ø  	   þ               2  0   5  0   f  ,     +   Ä     ð     ü               -     =     M     U     \     s     |            +   ¤  &   Ð     ÷               *     >  	   G     Q     Z     `  
   s     ~       
        §     ³     Ä     Ë     æ     ø     þ            t     $        ¹     ¿     Ö     â     ó               "     /     6     ;     K     c     j                    ¨     »     Ñ  1   à                 ,      >      O      `      o                   ·      Ö   O   ñ   6   A!     x!     !  .  °!  *  ß"  0  
&  ^  ;)  =   -     Ø-     ø-     	.     (.     G.     f.     .     ¤.     Ä.  ?   Ù.     /     7/  %   P/  '   v/  ?   /  E   Þ/     $0     10     80     E0  	   Z0     d0  	   k0     u0     0     0  	   0     ©0     ¶0     ½0     Ë0     Ò0     Ù0     à0     ç0  0   î0     1     >1  H   K1     1     1     ¢1     ¯1     Â1     Õ1     è1     ö1     2  	   2     2     '2     92  0   <2  6   m2  /   ¤2  (   Ô2     ý2     
3     3     *3     :3     M3     Z3     f3     m3     }3     3     3  	   3     ¢3     Á3     Ú3     ê3     ÷3     4  	   4     4  	   %4     /4     64     G4     T4     c4     p4     }4     4     4     4     ±4     Ä4     Ë4     Ò4     Ù4  i   ì4     V5     l5     s5     5     5     5      5     ©5     ¶5     Ã5     Ê5     Ñ5     Þ5     î5     õ5     6     6     "6     /6     <6     E6  /   R6     6     6     6     «6     ¸6     Å6     Ò6     å6     ø6     7     $7  O   C7  6   7     Ê7     æ7     6          X   J   !          L   s   %          |   N   P   @   b   -      K   e   p       F      /      >   c   ^   T      \       z       ,      :   
      i   U      r   [   <   W         8         4                              +   d   A           #           *   f   (      g   D       2       &          R   k   ?   `   3   M   x       n       H            }          l   a                     w       o   u           Q                                     h   )   t       Y   "   C   y      9   V   _   7   G   v                m   {       O           5      0   '   ]   1   S   =   $       	       B   ~          E   .                    I   ;         Z         q       j    
                
                    Congratulations <b>${object.partner_id.name},</b><br><br>
                    Your Wallet is credited with amount <b>${format_amount(object.amount, object.currency_id)}</b><br>
                    Tags: <b>${', '.join(object.tag_ids.mapped('name'))}</b><br>
                    Total Amount in Wallet <b>
                      ${format_amount(object.wallet_id.company_id.currency_id.compute(
                      object.partner_id.wallet_credit, object.env['res.users'].search([('partner_id','=',object.partner_id.id)]).company_id.currency_id), object.env['res.users'].search([('partner_id','=',object.partner_id.id)]).company_id.currency_id)}</b><br><br>
                    <br>
                    Regards<br>
                    ${object.env.user.name}
                
             
                
                    Dear <b>${object.partner_id.name},</b><br><br>
                    Your Wallet is Debited with amount <b>${format_amount(object.currency_id.round(object.amount), object.currency_id)}
                    </b><br>
                    Tags: ${', '.join(object.tag_ids.mapped('name'))}<br>
                    Remaining Amount in Wallet <b>${format_amount(object.wallet_id.company_id.currency_id.compute(
                      object.partner_id.wallet_credit, object.env['res.users'].search([('partner_id','=',object.partner_id.id)]).company_id.currency_id), object.env['res.users'].search([('partner_id','=',object.partner_id.id)]).company_id.currency_id)}
                    <br>
                    Regards<br>
                    ${object.env.user.name}
                
             
                
                    Dear <b>${object.partner_id.name},</b><br><br>
                    Your wallet transaction is accepted by ${object.env.user.company_id.name}
                    Wallet Debited with amount <b>${format_amount(object.currency_id.round(object.amount), object.currency_id}
                    <span>&asymp;</span>${format_amount(object.total_amount, object.currency_id}
                   </b><br>
                    Tags: ${', '.join(object.tag_ids.mapped('name'))}<br>
                    <p>Sale Orders:<b>${', '.join(object.sale_order_line_ids.mapped('product_id').mapped('name'))}</b><br>
                    Remaining Amount in Wallet <b>${format_amount(object.wallet_id.company_id.currency_id.compute(
                      object.partner_id.wallet_credit, object.env['res.users'].search([('partner_id','=',object.partner_id.id)]).company_id.currency_id), object.env['res.users'].search([('partner_id','=',object.partner_id.id)]).company_id.currency_id) </b><br><br>
                    <br>
                    Regards<br>
                    ${object.env.user.name}
                
             <b class="total-w-text">Your current E-Wallet balance is</b> <b>Pay Using E-Wallet</b> <b>Total:</b> <i class="fa fa-check"/> Credit <i class="fa fa-check"/> Done <i class="fa fa-check"/>Refunded <i class="fa fa-remove"/> Debit <i class="fa fa-remove"/> Draft <i class="fa fa-remove"/>Cancelled <span>Sort By:</span> <strong>E-Wallet:</strong>
                <span>(-)</span> <strong>E-Wallet</strong> <strong>Total:</strong> A journal must be specified of the acquirer %s. A payment acquirer is required to create a transaction. A transaction can't be linked to sales orders having different currencies. A transaction can't be linked to sales orders having different partners. Action Needed Active Amount In Your Amount Mismatch (%s) Attachment Count Cancel Cancelled Cancelled Sale Order Tag Company Contact Created by Created on Credit Credit/Debit Currency Customer Customers Date Debit Default Cancelled Sale Order Wallet Money Tag Default Sale Order Transaction Tag Display Name Display the converted amount from the currency used for transaction to the current wallet company currency Done Draft E-Wallet E-Wallet Amount E-Wallet Transactions E-Wallet amount E-Wallet: E-wallet: Error Followers Followers (Channels) Followers (Partners) ID If checked, new messages require your attention. If checked, some messages have a delivery error. Invalid token found! Token acquirer %s != %s Invalid token found! Token partner %s != %s Is Follower Journal Entries Last Modified on Last Updated by Last Updated on Main Attachment Manager Manual Message Delivery error Messages Name Number of Actions Number of errors Number of messages which requires an action Number of messages with delivery error Number of unread messages Pay Now Payment Acquirer Payment Transaction Provider Reference Refunded Reset SMS Delivery error Sale Order Sale Order ID Sale Order Line Sale_Order Sales Order Sales Order Line Search Search Transaction History Show Transactions State Tag Tags Terms and conditions... The order was not confirmed despite response from the acquirer (%s): order total is %r but acquirer replied with %r. There are currently no transactions. Total Total Converted Amount Transaction Transaction Date Transaction ID Transaction Id Transaction Tags Transactions Txn Id Type Unread Messages Unread Messages Counter Wallet Wallet Customers kanban Wallet Debit Wallet Image Wallet Name Wallet Transaction Wallet Transaction Id Wallet balance Wallet: received data with missing reference (%s) Website Website Customers Website Debit Tag Website E-Wallet Website Messages Website Wallet Website communication history wallet currency id website e wallet model website transaction tags model website transactions model äº¤æå®æï¼æ¨çç·ä¸ä»æ¬¾å·²æåèçå®ç¢ã æè¬æ¨çè¨è³¼ã æ¨çä»æ¬¾å·²æåèçï¼ä½æ­£å¨ç­å¾æ¹åã æ¨çä»æ¬¾å·²ç²ææ¬ã æ¨çä»æ¬¾å·²è¢«åæ¶ã Project-Id-Version: Odoo Server 13.0
Report-Msgid-Bugs-To: 
PO-Revision-Date: 2020-06-05 09:33+0800
Language-Team: 
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Plural-Forms: nplurals=1; plural=0;
X-Generator: Poedit 2.3.1
Last-Translator: 
Language: zh_TW
 
                
                    æ­åä½ <b>${object.partner_id.name},</b><br><br>
                    æ¨çé¢åè¢«å­æ¬¾éé¡ <b>${format_amount(object.amount, object.currency_id)}</b><br>
                    æ¨ç±¤: <b>${', '.join(object.tag_ids.mapped('name'))}</b><br>
                    é¢åä¸­çç¸½éé¡ <b>
                      ${format_amount(object.wallet_id.company_id.currency_id.compute(
                      object.partner_id.wallet_credit, object.env['res.users'].search([('partner_id','=',object.partner_id.id)]).company_id.currency_id), object.env['res.users'].search([('partner_id','=',object.partner_id.id)]).company_id.currency_id)}</b><br><br>
                    <br>
                    æ¬å<br>
                    ${object.env.user.name}
                
             
                
                    <b>${object.partner_id.name},</b> æ¨å¥½<br><br>
                    æ¨çé¢åè¢«æ£æ¬¾éé¡ <b>${format_amount(object.currency_id.round(object.amount), object.currency_id)}
                    </b><br>
                    æ¨ç±¤: ${', '.join(object.tag_ids.mapped('name'))}<br>
                    é¢åä¸­çå©é¤éé¡ <b>${format_amount(object.wallet_id.company_id.currency_id.compute(
                      object.partner_id.wallet_credit, object.env['res.users'].search([('partner_id','=',object.partner_id.id)]).company_id.currency_id), object.env['res.users'].search([('partner_id','=',object.partner_id.id)]).company_id.currency_id)}
                    <br>
                    æ¬å<br>
                    ${object.env.user.name}
                
             
                
                    <b>${object.partner_id.name},</b>æ¨å¥½<br><br>
                    ä½ çé¢åäº¤æè¢« ${object.env.user.company_id.name}æ¥å
                    é¢åå¢å éé¡ <b>${format_amount(object.currency_id.round(object.amount), object.currency_id}
                    <span>&asymp;</span>${format_amount(object.total_amount, object.currency_id}
                   </b><br>
                    æ¨ç±¤: ${', '.join(object.tag_ids.mapped('name'))}<br>
                    <p>é·å®è¨å®:<b>${', '.join(object.sale_order_line_ids.mapped('product_id').mapped('name'))}</b><br>
                   é¢åä¸­çå©é¤éé¡<b>${format_amount(object.wallet_id.company_id.currency_id.compute(
                      object.partner_id.wallet_credit, object.env['res.users'].search([('partner_id','=',object.partner_id.id)]).company_id.currency_id), object.env['res.users'].search([('partner_id','=',object.partner_id.id)]).company_id.currency_id) </b><br><br>
                    <br>
                    æ¬å<br>
                    ${object.env.user.name}
                
             <b class="total-w-text">æ¨ç®åçé»å­é¢åé¤é¡æ¯</b> <b>ä½¿ç¨é»å­é¢åä»æ¬¾</b> <b> åè¨: </b> <i class="fa fa-check"/>å­æ¬¾ <i class="fa fa-check"/>å®æ <i class="fa fa-check"/>éé <i class="fa fa-check"/>æ£æ¬¾ <i class="fa fa-check"/>èç¨¿ <i class="fa fa-remove"/>åæ¶ <span>æåº:</span> <strong>é»å­é¢å:</strong>
                <span>(-)</span> <strong>é»å­é¢å</strong> <strong>åè¨:</strong> å¿é æå®æ¶å®æ¹çæ¥è¨å¸³ %s. æ¯ä»æ¶å®æ©æ§éè¦å»ºç«äº¤æã äº¤æè¨éä¸è½é£çµå°å·æä¸åè²¨å¹£çé·å®è¨å®ã äº¤æè¨éä¸è½é£çµå°å·æä¸ååä½å¤¥ä¼´çé·å®è¨å®ã æéåä½ åä½ æ¨çéé¡ éé¡ä¸å¹é (%s) éä»¶æ¸ åæ¶ å·±æ¶å åæ¶çé·å®è¨å®æ¨ç±¤ å¬å¸ è¯ç¹« å»ºç«è å»ºç«æ¥æ å­æ¬¾ å­æ¬¾/æ£æ¬¾ è²¨å¹£ å®¢æ¶ å®¢æ¶ æ¥æ æ£æ¬¾ é è¨­å·²åæ¶çé·å®è¨å®é¢åè²¨å¹£æ¨ç±¤ é è¨­é·å®è¨å®äº¤ææ¨ç±¤ é¡¯ç¤ºåç¨± é¡¯ç¤ºå¾ç¨æ¼äº¤æçè²¨å¹£å°ç¶åé¢åå¬å¸è²¨å¹£çè½æéé¡ å®æ èç¨¿ é»å­é¢å é»å­é¢åéé¡ é»å­é¢åäº¤æ é»å­é¢åéé¡ é»å­é¢å: é»å­é¢å: é¯èª¤ éæ³¨è éæ³¨è(é »é) éæ³¨è(å¤¥ä¼´) ID å¦æå¾é¸ï¼ææ°çæ¶æ¯éè¦æ¨éæ³¨ã å¦æå¾é¸äºï¼æäºæ¶æ¯æåºç¾ééé¯èª¤ã ç¼ç¾ç¡ætoken ! token æ¶å®èçº %s != %s ç¼ç¾ç¡ætoken! Token å¤¥ä¼´ %s != %s æ¯éæ³¨è æ¥è¨æ¢ç® æå¾ä¿®æ¹æé æå¾æ´æ°è æå¾æ´æ°æé ä¸»è¦éä»¶ ç®¡çå¡
	 æå è¨å³éé¯èª¤ è¨æ¯ åç¨± è¡åæ¬¡æ¸ é¯èª¤æ¸ éè¦æ¡åæªæ½çæ¶æ¯æ¸ å³éé¯èª¤çè¨æ¯æ¸ æªè®è¨æ¯æ¸ ç«å³ä»æ¬¾ ä»æ¬¾æ¶æ¬¾äºº ä»æ¬¾äº¤æ æä¾è åè å·²éæ¬¾ éç½® SMS ç¼éé¯èª¤ é·å®è¨å® é·å®è¨å®ID é·å®æç´° é·å®è¨å® é·å®è¨å® é·å®æç´° æ¥è©¢ æ¥è©¢äº¤æè¨é é¡¯ç¤ºäº¤æè¨é çæ æ¨ç±¤ æ¨ç±¤ æ¢æ¬¾åæ¢ä»¶... åç®¡æ¶æ¬¾äººååºäºåæï¼ä½è¨å®ä»æªç¢ºèª (%s): è¨å®ç¸½æ¸çº %r ä½æ¯æ¶æ¬¾äººåè¦ %r. ç¶åæ²æäº¤æã åè¨ ç¸½è½æéé¡ äº¤æ äº¤ææ¥æ äº¤æID äº¤æID äº¤ææ¨ç±¤ äº¤æè¨é Txn Id é¡å æªè®è¨æ¯ æªè®è¨æ¯æ¸ é¢å é¢åå®¢æ¶çæ¿ é¢åæ£æ¬¾ é¢ååç é¢ååç¨± äº¤ææ¨ç±¤ äº¤æID é¢åé¤é¡ é»å­é¢åï¼æ¶å°çè³æç¼ºå°åè (%s) ç¶²ç« ç¶²ç«å®¢æ¶ ç¶²ç« æ£æ¬¾ æ¨ç±¤ é»å­é¢å ç¶²ç«è¨æ¯ é»å­é¢å ç¶²ç«äº¤æµæ­·å² é¢åè²¨å¹£ç·¨è é»å­é¢åæ¨¡çµ é»å­é¢åæ¨ç±¤æ¨¡çµ é»å­é¢åäº¤ææç´°æ¨¡çµ äº¤æå®æï¼æ¨çç·ä¸ä»æ¬¾å·²æåèçå®ç¢ã æè¬æ¨çè¨è³¼ã æ¨çä»æ¬¾å·²æåèçï¼ä½æ­£å¨ç­å¾æ¹åã æ¨çä»æ¬¾å·²ç²ææ¬ã æ¨çä»æ¬¾å·²è¢«åæ¶ã 
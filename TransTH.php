 <?php
 require_once "GoogleTranslate.php";
 $word = $_REQUEST['word'];
$GT = NEW GoogleTranslate();
$response = $GT->translate('th','en',$word);  /// ตรง en เราสามารถเปลี่ยนเป็น ภาษาอื่นได้
//echo "<pre>";
echo $word."   =   ".$response;
?>

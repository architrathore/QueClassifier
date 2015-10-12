<?php

require 'sanscript.php';
$sanscript = new Sanscript();
$output = $sanscript->t($argv[1],'devanagari','itrans');
echo strtolower($output);
?>
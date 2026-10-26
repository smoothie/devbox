<?php

header('Content-Type: application/json');
echo json_encode([
    'version' => PHP_VERSION,
    'sapi' => PHP_SAPI,
    'extensions' => array_map('strtolower', get_loaded_extensions()),
    'timezone' => date_default_timezone_get(),
    'memory_limit' => ini_get('memory_limit'),
    'xdebug_port' => ini_get('xdebug.client_port'),
], JSON_THROW_ON_ERROR);

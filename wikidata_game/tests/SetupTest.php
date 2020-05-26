<?php declare(strict_types=1);

/**
 * This file is meant to validate testing and ci setup and is therefore TEMPORARY. 
 * It should be replaced with a real test as soon as the first one is written.
 */
use PHPUnit\Framework\TestCase;

final class SetupTest extends TestCase
{
    public function testCanRunTests(): void
    {
        $this->assertTrue(true);
    }
}
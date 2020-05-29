<?php declare(strict_types=1);

use PHPUnit\Framework\TestCase;

require_once('util/helpers.php');

/**
 * @testdox array_has_keys()
 */
final class ArrayHasKeysTest extends TestCase
{
    protected $mock_array;

    protected function setUp(): void
    {
        $this->mock_array = ['hello' => '', 'test' => '', 'goodbye' => ''];
    }

    /**
     * @testdox Returns true if all keys are present
     */
    public function testAllKeysPresent(): void
    {
        $this->assertTrue(array_has_keys(['test', 'hello'], $this->mock_array));
    }

    /**
     * @testdox Returns false if one key is missing
     */
    public function testOneKeyMissing(): void
    {
        $this->assertFalse(array_has_keys(['coolsies', 'test', 'hello'], $this->mock_array));
    }
}
import { describe, it, expect } from 'vitest';

// Component structure test
describe('Component files', () => {
  it('Navbar component exists', async () => {
    const module = await import('../src/components/Navbar.jsx');
    expect(module).toBeDefined();
    expect(module.default).toBeDefined();
  });
});

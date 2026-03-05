import { describe, it, expect } from 'vitest';

// Verify that API service exports exist and have expected methods
describe('API Services', () => {
  it('articlesAPI should export expected methods', async () => {
    const { articlesAPI } = await import('../src/services/api');
    expect(typeof articlesAPI.getAll).toBe('function');
    expect(typeof articlesAPI.getOne).toBe('function');
    expect(typeof articlesAPI.create).toBe('function');
    expect(typeof articlesAPI.like).toBe('function');
    expect(typeof articlesAPI.trending).toBe('function');
  });

  it('authAPI should export expected methods', async () => {
    const { authAPI } = await import('../src/services/api');
    expect(typeof authAPI.register).toBe('function');
    expect(typeof authAPI.login).toBe('function');
  });

  it('bookmarksAPI should export expected methods', async () => {
    const { bookmarksAPI } = await import('../src/services/api');
    expect(typeof bookmarksAPI.getAll).toBe('function');
    expect(typeof bookmarksAPI.create).toBe('function');
    expect(typeof bookmarksAPI.remove).toBe('function');
  });
});

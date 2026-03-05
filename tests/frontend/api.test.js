import { describe, it, expect, vi } from 'vitest';
import { articlesAPI, authAPI, bookmarksAPI } from '../../frontend/src/services/api';
import axios from 'axios';

vi.mock('axios');

describe('articlesAPI', () => {
  it('getAll should return data array', async () => {
    axios.get.mockResolvedValue({ data: [{ id: 1, title: 'A' }] });
    const res = await articlesAPI.getAll();
    expect(res.data).toEqual([{ id: 1, title: 'A' }]);
  });
});

describe('authAPI', () => {
  it('register should forward data', async () => {
    const form = { username: 'u', email: 'e', password: 'p' };
    axios.post.mockResolvedValue({ data: { id: 1, username: 'u' } });
    const res = await authAPI.register(form);
    expect(axios.post).toHaveBeenCalledWith('/register/', form);
    expect(res.data.username).toBe('u');
  });
});

describe('bookmarksAPI', () => {
  it('create sends article id', async () => {
    axios.post.mockResolvedValue({ data: { message: 'ok' } });
    const res = await bookmarksAPI.create(5);
    expect(axios.post).toHaveBeenCalledWith('/bookmarks/', { article_id: 5 });
    expect(res.data.message).toBe('ok');
  });
});

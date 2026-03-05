import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import Navbar from '../../frontend/src/components/Navbar';

// simple smoke test for Navbar

describe('Navbar component', () => {
  it('renders links', () => {
    render(<Navbar />);
    // assume there is a home link
    const homeLink = screen.getByText(/home/i);
    expect(homeLink).toBeInTheDocument();
  });
});
